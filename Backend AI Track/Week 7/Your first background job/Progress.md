# Progress — Your First Background Job (A7)

Lane: **[ JS / Python ]**
Repo: **[ link ]**

---

## Stage 0 — Hello, server
**Goal:** `GET /health` → `{ "status": "ok" }`

- [OK] Server starts (`Express :3000` / `FastAPI :8000`)
- [OK] Checkpoint run:
  ```
  $ curl -i http://localhost:3000/health
  [paste output here]
  ```
- [OK] Committed: `Stage 0: hello server`

Notes:

(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship>curl -i http://localhost:8000/health     
HTTP/1.1 200 OK
date: Wed, 26 Aug 2026 07:07:05 GMT
server: uvicorn
content-length: 15
content-type: application/json

{"status":"ok"}

---

## Stage 1 — Hire the worker: connect Inngest
**Goal:** Inngest client + `say-hello` function (sleep 5s) wired at `/api/inngest`

- [ ] `inngest` installed
- [ ] Client created (id: `report-api`)
- [ ] Function `say-hello` created, triggered by `test/hello`
- [ ] Dev Server running: `npx inngest-cli@latest dev -u http://localhost:3000/api/inngest`
- [ ] Dashboard (`localhost:8288`) shows `say-hello` run → **Completed**
- [ ] Screenshot / notes on the run:
- [ ] Committed: `Stage 1: Inngest connected, first function runs`

Notes:

---

## Stage 2 — The fast door: accept now, work later
**Goal:** `POST /reports` returns 202 instantly; `make-report` does the 8s work; `GET /reports/:id` polls status

- [ ] In-memory `reports` store created
- [ ] `POST /reports` validates input, sends `report/requested` event, returns `202`
- [ ] `make-report` function: `step.sleep("do-the-slow-work", "8s")` → `step.run("build-report", ...)`
- [ ] `GET /reports/:id` returns `pending` then `done`; unknown id → `404`
- [ ] Checkpoint run (timed POST):
  ```
  $ time curl -i -X POST http://localhost:3000/reports -H "Content-Type: application/json" -d '{"topic":"cats"}'
  [paste output + timing here]
  ```
- [ ] Checkpoint run (poll ~10s later):
  ```
  $ curl -i http://localhost:3000/reports/<id>
  [paste "pending" output]
  [paste "done" output, ~10s later]
  ```
- [ ] Committed: `Stage 2: 202 + background job + status endpoint`

Notes:

---

## Stage 3 — Jobs fail. Watch the retry.
**Goal:** `topic: "fail"` triggers 3 attempts (retries: 2), ends Failed; bad input is 400, no job

- [ ] `build-report` throws when `topic === "fail"`
- [ ] Function config: `retries: 2`
- [ ] Dashboard shows: attempt 1 fail → wait → attempt 2 → attempt 3 → **Failed**
  - Screenshot / notes:
- [ ] `POST /reports` with no `topic` → `400`, no event sent
  ```
  $ curl -i -X POST http://localhost:3000/reports -H "Content-Type: application/json" -d '{}'
  [paste output here]
  ```
- [ ] README sentence written: *why retries ≠ validation*
  > [your sentence here]
- [ ] Committed: `Stage 3: retries seen, bad input rejected`

Notes:

---

## Stage 4 — The clock knocks: your first cron job
**Goal:** `heartbeat` function runs every minute on a cron trigger, logs pending/done/failed counts

- [ ] `heartbeat` function created with schedule `* * * * *`
- [ ] Logs one summary line per run (pending / done / failed counts)
- [ ] Dashboard shows ≥2 `heartbeat` runs, 1 minute apart
  - Screenshot / notes:
- [ ] README sentences written:
  - Cron for "every day at 08:00": `[expression]`
  - Cron for "every Sunday at 22:00": `[expression]`
- [ ] Committed: `Stage 4: cron heartbeat`

Notes:

---

## Stage 5 — Publish to GitHub
**Goal:** public repo + README a stranger can run in <5 min

- [ ] Repo is public: `[link]`
- [ ] README includes:
  - [ ] What this is
  - [ ] How to run (2 commands: API + Dev Server)
  - [ ] Endpoint/function table
  - [ ] Pasted 202 + poll proof
  - [ ] Stage 3 sentence
  - [ ] Stage 4 sentences
  - [ ] Dashboard screenshot
- [ ] Committed: `Stage 5: publish and docs`

Notes:

---

## ★ Optional extras (pick any)
- [ ] `GET /reports` list endpoint
- [ ] "Email" — writes result to `outbox/<id>.txt`
- [ ] Cleanup cron — deletes done reports older than 10 min
- [ ] Custom heartbeat schedule (note what it means)
- [ ] Restart experiment — notes below

Notes:

---

## Stage 6 (Bonus) — The AI rematch

- [ ] My own prompt written from memory (no copying from the assignment doc):
  ```
  [paste your prompt here]
  ```
- [ ] AI code generated in `ai-version/` (separate folder/branch)
- [ ] Ran Stage 2 checkpoint against AI version — pass/fail: `[ ]`
- [ ] Ran Stage 3 checkpoint against AI version — pass/fail: `[ ]`
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
- [ ] Committed: `Stage 6: AI vs me`

---

## Stretch goals (optional)
- [ ] Idempotency check (same event id sent twice → built once) + README line
- [ ] Concurrency limit (max 2 at once, 5 enqueued, 3 wait)
- [ ] Durable restart proof (3-step function, screenshot: finished steps didn't re-run)

---

## Final "Done means" checklist
- [ ] 202 proof pasted in README
- [ ] Dashboard screenshot: completed run, failed run w/ retries, cron runs
- [ ] Repo public, README works on a clean machine, ≥6 honest commits
- [ ] API + Dev Server each start with one documented command
- [ ] `POST /reports` → 202 + id, in <1s
- [ ] `GET /reports/:id` → pending → done; 404 unknown; 400 missing topic
- [ ] `make-report` has ≥2 steps, visible in dashboard
- [ ] `topic: "fail"` → 3 attempts, Failed
- [ ] Cron runs every minute, logs summary
- [ ] README complete (commands, table, proof, sentences, screenshot)