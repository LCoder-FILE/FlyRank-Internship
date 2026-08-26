from datetime import date
from report_data import get_report_data
from playwright.sync_api import sync_playwright

def build_html(data: dict) -> str:
    top_5_rows = "".join(
        f"<tr><td>{b['title']}</td><td>${b['price']:.2f}</td></tr>"
        for b in data["top_5_expensive"]
    )

    rating_rows = "".join(
        f"<tr><td>{r['rating']} stars</td><td>{r['count']}</td></tr>"
        for r in data["books_per_rating"]
    )

    all_books_rows = "".join(
        f"<tr><td>{b['title']}</td><td>${b['price']:.2f}</td><td>{b['rating']} stars</td></tr>"
        for b in data["all_books"]
    )

    return f"""
    <html>
    <head>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        h1 {{ margin-bottom: 0; }}
        .subtitle {{ color: #666; margin-top: 4px; }}
        .totals {{ display: flex; gap: 40px; margin: 20px 0; }}
        .totals div {{ font-size: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ border: 1px solid #ccc; padding: 6px 10px; text-align: left; }}
        thead {{ display: table-header-group; }}
        tr {{ break-inside: avoid; }}
        h2 {{ margin-top: 30px; }}
    </style>
    </head>
    <body>
        <h1>Bookstore Report</h1>
        <div class="subtitle">Generated on {date.today().isoformat()}</div>

        <div class="totals">
            <div><strong>Total books:</strong> {data['total_books']}</div>
            <div><strong>Average price:</strong> ${data['average_price']:.2f}</div>
        </div>

        <h2>Top 5 Most Expensive Books</h2>
        <table>
            <thead><tr><th>Title</th><th>Price</th></tr></thead>
            <tbody>{top_5_rows}</tbody>
        </table>

        <h2>Books per Rating</h2>
        <table>
            <thead><tr><th>Rating</th><th>Count</th></tr></thead>
            <tbody>{rating_rows}</tbody>
        </table>

        <h2>All Books</h2>
        <table>
            <thead><tr><th>Title</th><th>Price</th><th>Rating</th></tr></thead>
            <tbody>{all_books_rows}</tbody>
        </table>
    </body>
    </html>
    """


def render_pdf(html: str, output_path: str):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html)
        page.pdf(path=output_path, format="A4", print_background=True)
        browser.close()

if __name__ == "__main__":
    data = get_report_data()
    html = build_html(data)
    render_pdf(html, "reports/test.pdf")
    print("Saved reports/test.pdf")