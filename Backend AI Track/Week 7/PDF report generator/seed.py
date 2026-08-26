import json
import sqlite3
from pathlib import Path

DB_PATH = "report.db"
BOOKS_JSON_PATH = "./datasets/books.json"  # adjust if your A9 file lives elsewhere

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_schema(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price REAL NOT NULL,
            rating INTEGER NOT NULL,
            url TEXT NOT NULL
        )
    """)
    conn.commit()

def seed(conn):
    # Safe to run twice: clear existing rows first
    conn.execute("DELETE FROM books")
    conn.commit()

    with open(BOOKS_JSON_PATH, "r", encoding="utf-8") as f:
        books = json.load(f)

    for book in books:
        conn.execute(
            "INSERT INTO books (title, price, rating, url) VALUES (?, ?, ?, ?)",
            (book["title"], book["price_gbp"], book["rating"], book["detail_url"]),
        )
    conn.commit()

if __name__ == "__main__":
    conn = get_connection()
    create_schema(conn)
    seed(conn)

    count = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    print(f"Seeded {count} books.")
    conn.close()