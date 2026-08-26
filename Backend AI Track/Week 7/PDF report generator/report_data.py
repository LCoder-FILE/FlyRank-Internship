import sqlite3
import json

DB_PATH = "report.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_report_data():
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    all_books = conn.execute(
        "SELECT title, price, rating FROM books ORDER BY title"
    ).fetchall()
    all_books = [dict(row) for row in all_books]

    total_books = conn.execute(
        "SELECT COUNT(*) AS count FROM books"
    ).fetchone()["count"]

    avg_price = conn.execute(
        "SELECT AVG(price) AS avg_price FROM books"
    ).fetchone()["avg_price"]

    top_5 = conn.execute(
        "SELECT title, price FROM books ORDER BY price DESC LIMIT 5"
    ).fetchall()
    top_5 = [dict(row) for row in top_5]

    per_rating = conn.execute(
        "SELECT rating, COUNT(*) AS count FROM books GROUP BY rating ORDER BY rating"
    ).fetchall()
    per_rating = [dict(row) for row in per_rating]

    conn.close()

    return {
        "all_books": all_books,
        "total_books": total_books,
        "average_price": round(avg_price, 2) if avg_price else 0,
        "top_5_expensive": top_5,
        "books_per_rating": per_rating,
    }



if __name__ == "__main__":
    data = get_report_data()
    print(json.dumps(data, indent=2))