# Progress — PDF Report Generator

Lane: **[ JS / Python ]**
Dataset: **[ Shop (orders) / Bookstore (A9 books.json) ]**
Repo: **[ link ]**

---

## Stage 0 — The setup
**Goal:** `GET /health` → `{ "status": "ok" }`, Playwright + Chromium installed

- [x] Server starts (`Express :3000` / `FastAPI :8000`)
- [x] Playwright installed: `pip install playwright` / `npm install playwright`
- [x] Chromium installed: `playwright install chromium` / `npx playwright install chromium`
- [x] Checkpoint run:
  ```
  $ curl -i http://localhost:8000/health
    HTTP/1.1 200 OK
    date: Wed, 26 Aug 2026 12:46:16 GMT
    server: uvicorn
    content-length: 15
    content-type: application/json

    {"status":"ok"}
  ```
- [x] `playwright install chromium` finished without errors
- [x] Committed: `Stage 0: setup ready`

Notes:

---

## Stage 1 — Data worth reporting on
**Goal:** `report.db` seeded, idempotent (running seed twice ≠ double rows)

- [x] Dataset chosen: **[ Shop / Bookstore ]**
- [x] `report.db` created with table (`orders` or `books`)
- [x] `seed` script writes ~200 orders (or 60 books)
- [x] Seed script deletes existing rows first (safe to run twice)
- [x] Checkpoint — ran seed twice, row count still correct:
  ```
  $ [seed command] && [seed command]
  $ [query command] -> SELECT COUNT(*)
  
    FlyRank-Internship\Backend AI Track\Week 7\PDF report generator>python seed.py
    Seeded 100 books.

    FlyRank-Internship\Backend AI Track\Week 7\PDF report generator>python seed.py
    Seeded 100 books.

    FlyRank-Internship\Backend AI Track\Week 7\PDF report generator>sqlite3 report.db "SELECT COUNT(*) FROM books;"
    ╭──────────╮
    │ COUNT(*) │
    ╞══════════╡
    │      100 │
    ╰──────────╯

  ```
- [x] Committed: `Stage 1: seeded report.db`

Notes:

---

## Stage 2 — Boring SQL is 80% of reporting
**Goal:** `getReportData()` returns totals, top 5, and a grouped breakdown

- [ ] Query: total count
- [ ] Query: total revenue (`SUM`) / average price (`AVG`)
- [ ] Query: top 5 (products by revenue / books by price)
- [ ] Query: grouped breakdown (orders per day last 7 days / books per rating)
- [ ] All four combined into one `getReportData()` function
- [ ] Checkpoint — test script prints full report object:
  ```
  [paste JSON output here]
  ```
- [ ] Sanity-checked the numbers make sense (e.g. no single product's revenue > total)
- [ ] Committed: `Stage 2: aggregation queries`

Notes:

---

## Stage 3 — Render: from numbers to a PDF
**Goal:** `reports/test.pdf` — ≥2 pages, no row cut by a page break, header repeats

- [ ] HTML template built from report object (title + date, totals, top-5 table, long table)
- [ ] Playwright renders HTML → PDF (`reports/test.pdf`)
- [ ] Found the page-break trap (a row sliced in half)
- [ ] Fixed with print CSS: `tr { break-inside: avoid; }` + `<thead>` repeats per page
- [ ] Checkpoint — opened `reports/test.pdf`:
  - Pages: **[ n ]**
  - No row cut in half: **[ yes/no ]**
  - Header repeats on page 2+: **[ yes/no ]**
- [ ] Committed: `Stage 3: HTML to PDF with clean page breaks`

Notes:

---

## Stage 4 — Serve it from your API
**Goal:** `POST /reports` generates + returns link; `GET /reports/:id/file` downloads the PDF

- [ ] `reports` table added to `report.db` (`id`, `path`, `created_at`)
- [ ] `POST /reports` — runs query → render → save row, returns `201` + `{id, file}`
- [ ] `GET /reports/:id` → the row + file link; unknown id → `404`
- [ ] `GET /reports/:id/file` → serves the PDF from disk
- [ ] Checkpoint (timed POST):
  ```
  $ time curl -i -X POST http://localhost:8000/reports
  [paste output + timing — note the visible pause]
  ```
- [ ] Checkpoint (download):
  ```
  $ curl -o my-report.pdf http://localhost:8000/reports/<id>/file
  [confirm file opens as a real PDF]
  ```
- [ ] README sentence written: *at what point would you move this to a background job?*
  > [your sentence here]
- [ ] Committed: `Stage 4: generate and serve by link`

Notes:

---

## Stage 5 — Ask twice, get one
**Goal:** Two rapid `POST /reports` → same id, one new file; `force: true` → new id

- [ ] `POST /reports` checks for an existing report from today before generating
- [ ] Same-day duplicate → returns existing `id` + link with `200` (not `201`)
- [ ] `{ "force": true }` bypasses the check and generates a new one
- [ ] Checkpoint — two rapid POSTs:
  ```
  $ curl -i -X POST http://localhost:8000/reports
  $ curl -i -X POST http://localhost:8000/reports
  [paste both responses — same id?]
  ```
  - Only one new file appeared in `reports/`: **[ yes/no ]**
- [ ] Checkpoint — with `force: true`:
  ```
  $ curl -i -X POST http://localhost:8000/reports -d '{"force": true}'
  [paste output — new id?]
  ```
- [ ] README sentences written:
  1. What this check protects against:
     > [your sentence]
  2. Real-world example where a missing check like this costs money:
     > [your sentence]
- [ ] Committed: `Stage 5: duplicate requests make one report`

Notes:

---

## Stage 6 — Publish to GitHub
**Goal:** public repo + README a stranger can run in <5 min

- [ ] `reports/` and `report.db` added to `.gitignore`
- [ ] Repo is public: `[link]`
- [ ] README includes:
  - [ ] What this is + dataset chosen
  - [ ] How to run (seed command + API command)
  - [ ] Pasted aggregation SQL
  - [ ] POST → download proof
  - [ ] Stage 4 sentence
  - [ ] Stage 5 sentences
  - [ ] Screenshot of page 1 of a generated PDF
- [ ] Committed: `Stage 6: publish and docs`

Notes:

---

## ★ Optional extras (pick any)
- [ ] Pretty report (logo, brand colors, footer with page numbers)
- [ ] Parameterized report (`{"days": 7}` or `{"min_rating": 4}`)
- [ ] `GET /reports` — list all generated reports
- [ ] Nice filenames (e.g. `sales-report-2026-08-17.pdf`)
- [ ] Big-table experiment (5,000 rows) — notes on timing below

Notes:

---

## Stage 7 (Bonus) — The AI rematch

- [ ] My own prompt written from memory (no copying from the assignment doc):
  ```
  [paste your prompt here]
  ```
- [ ] AI code generated in `ai-version/` (separate folder/branch)
- [ ] Ran Stage 4 checkpoint against AI version — pass/fail: `[ ]`
- [ ] Ran Stage 5 checkpoint against AI version — pass/fail: `[ ]`
- [ ] Does the AI's PDF survive the page-break trap? `[ yes/no ]`
- [ ] `git diff --no-index` done
- [ ] "AI vs me" answers:
  1. What did the AI do better (and do I understand it)?
     >
  2. What did it get wrong or silently ignore?
     >
  3. What did my prompt forget to specify — what did the AI decide for me?
     >
- [ ] One rematch: improved prompt, regenerated, noted what changed
     >
- [ ] Committed: `Stage 7: AI vs me`

---

## Stretch goals (optional)
- [ ] Bring in A7: `POST /reports` → `202` instantly, Inngest function does query→render→save as steps, `GET /reports/:id` shows pending/done
      — README line: what got better for the user, what got more complex for you?
- [ ] Cron it: generate the report every Monday at 08:00, no request involved
      — README line: what happens to Monday's report if the server was down at 08:00?
- [ ] Email it: Mailpit catches an email with the report **link** (not attachment)
      — README line: why links beat attachments

---

## Final "Done means" checklist
- [ ] `report.db` seeded correctly even when seed is run twice
- [ ] Aggregation queries (two totals, top 5, grouped breakdown) pasted in README
- [ ] PDF renders from real data, ≥2 pages, no row cut, header repeats
- [ ] `POST /reports` → `201` + id + file link; `GET /reports/:id` → record; unknown id → `404`
- [ ] File served by link only — JSON responses never carry file bytes
- [ ] Duplicate requests same day → same id, one new file
- [ ] Repo public, ≥7 commits, README complete, `reports/` + `report.db` gitignored