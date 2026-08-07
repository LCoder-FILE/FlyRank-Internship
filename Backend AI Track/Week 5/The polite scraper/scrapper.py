"""
scraper.py
----------
A well-behaved scraper for https://books.toscrape.com — a public site built
specifically for scraping practice, so it's safe to point real code at.

Pipeline: fetch -> parse -> extract -> clean -> structure -> save

Behaves like a bot a site owner would tolerate:
  - Checks robots.txt before fetching EVERY url (not just once at the start)
  - Identifies itself with a real, descriptive User-Agent
  - Rate-limits requests (delay + jitter) instead of hammering the server
  - Retries with backoff on transient failures, then gives up gracefully
  - Times out requests instead of hanging forever
  - Saves progress incrementally, so a crash/interrupt doesn't lose everything

Usage:
    python scraper.py --pages 5 --out books

Output:
    books.csv
    books.json
    (both are rewritten after every listing page, so partial runs are safe)
"""

import argparse
import csv
import json
import logging
import random
import re
import time
from dataclasses import asdict, dataclass
from typing import List, Optional, Tuple
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
# Real contact info in the UA is the polite norm — it lets a site owner
# reach out instead of just blocking your IP if something goes wrong.
# NOTE: replace with a real contact before pointing this at any other site.
USER_AGENT = (
    "PracticeScraperBot/1.0 "
    "(+https://example.com/bot-info; contact: your-email@example.com)"
)
REQUEST_TIMEOUT = 10              # seconds
MIN_DELAY, MAX_DELAY = 1.5, 3.0   # polite rate-limit window, in seconds
MAX_RETRIES = 3

RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("scraper")


@dataclass
class Book:
    title: str
    price_gbp: float
    availability: str
    in_stock: bool
    rating: int
    category_url: str
    detail_url: str


class RobotsGate:
    """Downloads robots.txt once, then answers per-URL permission checks
    cheaply from the already-parsed rules. Fails closed: if robots.txt
    can't be read at all, nothing is considered fetchable."""

    def __init__(self, base_url: str, user_agent: str):
        self.user_agent = user_agent
        self.parser: Optional[RobotFileParser] = None
        rp = RobotFileParser()
        rp.set_url(urljoin(base_url, "/robots.txt"))
        try:
            rp.read()
            self.parser = rp
            log.info("Loaded robots.txt from %s", rp.url)
        except Exception as e:
            log.warning("Could not read robots.txt (%s); all fetches will be blocked.", e)

    def allowed(self, url: str) -> bool:
        if self.parser is None:
            return False
        ok = self.parser.can_fetch(self.user_agent, url)
        if not ok:
            log.warning("robots.txt disallows fetching %s", url)
        return ok


def polite_get(session: requests.Session, url: str) -> Optional[requests.Response]:
    """Fetch a URL with retries, backoff, and respect for 429 rate-limiting."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = session.get(url, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 200:
                return resp
            if resp.status_code == 429:
                wait = int(resp.headers.get("Retry-After", 5))
                log.warning("429 rate-limited on %s, waiting %ss", url, wait)
                time.sleep(wait)
                continue
            log.warning("Non-200 status %s for %s (attempt %d)", resp.status_code, url, attempt)
        except requests.RequestException as e:
            log.warning("Request failed for %s (attempt %d): %s", url, attempt, e)
        time.sleep(2 ** attempt)  # exponential backoff between retries
    log.error("Giving up on %s after %d attempts", url, MAX_RETRIES)
    return None


def rate_limit_sleep():
    time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))


def parse_listing_page(soup: BeautifulSoup, page_url: str) -> List[str]:
    """Extract detail-page links from an already-parsed listing/category page."""
    links = []
    for article in soup.select("article.product_pod"):
        a = article.select_one("h3 a")
        if a and a.get("href"):
            links.append(urljoin(page_url, a["href"]))
    return links


def get_next_page_url(soup: BeautifulSoup, page_url: str) -> Optional[str]:
    next_link = soup.select_one("li.next a")
    if next_link and next_link.get("href"):
        return urljoin(page_url, next_link["href"])
    return None


def clean_price(raw_price: str) -> float:
    """'£53.74' -> 53.74. Strips currency symbols/whitespace."""
    cleaned = re.sub(r"[^\d.]", "", raw_price)
    return float(cleaned) if cleaned else 0.0


def clean_availability(raw_text: str) -> Tuple[str, bool]:
    """'\n\n    In stock (22 available)\n    ' -> ('In stock (22 available)', True)"""
    text = " ".join(raw_text.split())
    in_stock = "in stock" in text.lower()
    return text, in_stock


def parse_detail_page(html: str, detail_url: str, category_url: str) -> Optional[Book]:
    """Extract and clean a single book's fields from its detail page.
    Returns None (and logs exactly which field was missing) instead of
    silently dying, so structural breakage is easy to diagnose."""
    soup = BeautifulSoup(html, "html.parser")

    title_tag = soup.select_one("div.product_main h1")
    if title_tag is None:
        log.warning("Missing title on %s, skipping", detail_url)
        return None
    title = title_tag.get_text(strip=True)

    price_tag = soup.select_one("p.price_color")
    if price_tag is None:
        log.warning("Missing price on %s, skipping", detail_url)
        return None
    price = clean_price(price_tag.get_text(strip=True))

    avail_tag = soup.select_one("p.availability")
    if avail_tag is None:
        log.warning("Missing availability on %s, skipping", detail_url)
        return None
    availability, in_stock = clean_availability(avail_tag.get_text())

    rating_tag = soup.select_one("p.star-rating")
    rating_word = None
    if rating_tag is not None:
        rating_word = next(
            (c for c in rating_tag.get("class", []) if c in RATING_WORDS), None
        )
    rating = RATING_WORDS.get(rating_word, 0)  # 0 = rating not found, not an error

    return Book(
        title=title,
        price_gbp=price,
        availability=availability,
        in_stock=in_stock,
        rating=rating,
        category_url=category_url,
        detail_url=detail_url,
    )


def save_csv(books: List[Book], path: str):
    if not books:
        log.warning("No books to save to CSV.")
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(books[0]).keys()))
        writer.writeheader()
        for b in books:
            writer.writerow(asdict(b))


def save_json(books: List[Book], path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(b) for b in books], f, indent=2, ensure_ascii=False)


def checkpoint(books: List[Book], out_prefix: str):
    """Rewrite output files with progress so far. Cheap enough to call
    after every listing page — means a crash/Ctrl-C never loses more than
    one page's worth of work."""
    save_csv(books, f"{out_prefix}.csv")
    save_json(books, f"{out_prefix}.json")
    log.info("Checkpoint: %d records saved to %s.csv / .json", len(books), out_prefix)


def crawl(max_pages: int, out_prefix: str) -> List[Book]:
    gate = RobotsGate(BASE_URL, USER_AGENT)
    if not gate.allowed(BASE_URL):
        log.error("robots.txt disallows crawling the start page. Stopping.")
        return []

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    books: List[Book] = []
    page_url = BASE_URL
    page_num = 1

    try:
        while page_url and page_num <= max_pages:
            if not gate.allowed(page_url):
                log.warning("Skipping disallowed listing page %s", page_url)
                break

            log.info("Fetching listing page %d: %s", page_num, page_url)
            resp = polite_get(session, page_url)
            if resp is None:
                break
            rate_limit_sleep()

            soup = BeautifulSoup(resp.text, "html.parser")  # parsed once, reused below
            detail_links = parse_listing_page(soup, page_url)
            log.info("Found %d books on page %d", len(detail_links), page_num)

            for link in detail_links:
                if not gate.allowed(link):
                    log.warning("Skipping disallowed detail page %s", link)
                    continue
                detail_resp = polite_get(session, link)
                rate_limit_sleep()
                if detail_resp is None:
                    continue
                book = parse_detail_page(detail_resp.text, link, page_url)
                if book is not None:
                    books.append(book)

            next_url = get_next_page_url(soup, page_url)
            page_num += 1
            page_url = next_url

            checkpoint(books, out_prefix)  # save progress after every page

    except KeyboardInterrupt:
        log.warning("Interrupted by user — saving progress collected so far.")
    finally:
        checkpoint(books, out_prefix)

    return books


def main():
    parser = argparse.ArgumentParser(description="Polite scraper for books.toscrape.com")
    parser.add_argument("--pages", type=int, default=3, help="Max listing pages to crawl")
    parser.add_argument("--out", type=str, default="books", help="Output filename (no extension)")
    args = parser.parse_args()

    books = crawl(max_pages=args.pages, out_prefix=args.out)
    log.info("Done. Collected %d records.", len(books))


if __name__ == "__main__":
    main()

    # to run : python scrapper.py --pages 5 --out books