import json
import sqlite3
import uuid

from datetime import datetime, date
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi import Body

from report_data import get_report_data
from render import build_html, render_pdf
from pydantic import BaseModel


# Application setup

app = FastAPI()

DB_PATH = "report.db"
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def ensure_reports_table():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id TEXT PRIMARY KEY,
            path TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

ensure_reports_table()



# GET Functions

@app.get("/health")
def get_health():
    return { "status": "ok" } 


@app.get("/reports/{report_id}")
def get_report(report_id: str):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM reports WHERE id = ?", (report_id,)
    ).fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="report not found")

    return {
        "id": row["id"],
        "created_at": row["created_at"],
        "file": f"/reports/{row['id']}/file",
    }

@app.get("/reports/{report_id}/file")
def get_report_file(report_id: str):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM reports WHERE id = ?", (report_id,)
    ).fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="report not found")

    return FileResponse(
        path=row["path"],
        media_type="application/pdf",
        filename=f"{report_id}.pdf",
    )



# POST Functions

class ReportRequest(BaseModel):
    force: bool = False

@app.post("/reports", status_code=201)
def create_report(body: ReportRequest = ReportRequest()):
    force = body.force
    today = date.today().isoformat()

    conn = get_connection()

    if not force:
        existing = conn.execute(
            "SELECT * FROM reports WHERE created_at LIKE ? ORDER BY created_at DESC LIMIT 1",
            (f"{today}%",),
        ).fetchone()

        if existing is not None:
            conn.close()
            return JSONResponse(
                status_code=200,
                content={"id": existing["id"], "file": f"/reports/{existing['id']}/file"},
            )

    report_id = str(uuid.uuid4())
    pdf_path = REPORTS_DIR / f"{report_id}.pdf"

    data = get_report_data()
    html = build_html(data)
    render_pdf(html, str(pdf_path))

    conn.execute(
        "INSERT INTO reports (id, path, created_at) VALUES (?, ?, ?)",
        (report_id, str(pdf_path), datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()

    return {"id": report_id, "file": f"/reports/{report_id}/file"}



# run setup : set PLAYWRIGHT_BROWSERS_PATH=D:\ms-playwright
# to run : fastapi dev server.py