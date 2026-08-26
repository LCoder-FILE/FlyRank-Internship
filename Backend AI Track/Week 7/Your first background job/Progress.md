# Progress — Your First Background Job (A7)

Lane: **[ JS / Python ]**
Repo: **[ link ]**

---

## Stage 0 — Hello, server
**Goal:** `GET /health` → `{ "status": "ok" }`

- [OK] Server starts (`Express :8000` / `FastAPI :8000`)
- [OK] Checkpoint run:
  ```
  $ curl -i http://localhost:8000/health
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

- [OK] `inngest` installed
- [OK] Client created (id: `report-api`)
- [OK] Function `say-hello` created, triggered by `test/hello`
- [OK] Dev Server running: `npx inngest-cli@latest dev -u http://localhost:8000/api/inngest`
- [OK] Dashboard (`localhost:8288`) shows `say-hello` run → **Completed**
- [OK] Screenshot / notes on the run:
- [OK] Committed: `Stage 1: Inngest connected, first function runs`

Notes:

[07:43:13.866] INF apps synced, disabling auto-discovery
[07:45:04.140] INF publishing event caller=devserver event_name=inngest/function.invoked internal_id=01M0YGF74CG5P0C66CHCBVN164 external_id=01M0YGF74CVQJTTSMVX2CBJ3MJ event="{ID:01M0YGF74CVQJTTSMVX2CBJ3MJ Name:inngest/function.invoked Data:map[_inngest:{InvokeType: InvokeIdempotencyKey: SourceAppID: SourceFnID: SourceFnVersion:0 InvokeFnID:report-api-say-hello InvokeCorrelationId: InvokeTraceCarrier:<nil> InvokeSpanRef:<nil> InvokeExpiresAt:0 InvokeGroupID: InvokeDisplayName: DebugSessionID:<nil> DebugRunID:<nil>}] Timestamp:1787730304140 Version: Meta:{Sessions:map[] PropagatedSessions:map[] sessionTombstones:[] clearPropagated:false} User:map[] size:0}"
[07:45:04.279] INF received event event=inngest/function.invoked event_id=01M0YGF74CVQJTTSMVX2CBJ3MJ internal_id=01M0YGF74CG5P0C66CHCBVN164
[07:45:04.280] INF initializing fn event=inngest/function.invoked event_id=01M0YGF74CVQJTTSMVX2CBJ3MJ internal_id=01M0YGF74CG5P0C66CHCBVN164 function=say-hello function_id=4e18be14-9017-56fd-b596-aa2b90c110d5
[07:45:09.538] INF received event event=inngest/function.finished event_id=01M0YGFCA56BTMV1AMJG8JFM6N internal_id=01M0YGFCA5RG8111PRT1ZE2TF9

---

## Stage 2 — The fast door: accept now, work later
**Goal:** `POST /reports` returns 202 instantly; `make-report` does the 8s work; `GET /reports/:id` polls status

- [OK] In-memory `reports` store created
- [OK] `POST /reports` validates input, sends `report/requested` event, returns `202`
- [OK] `make-report` function: `step.sleep("do-the-slow-work", "8s")` → `step.run("build-report", ...)`
- [OK] `GET /reports/:id` returns `pending` then `done`; unknown id → `404`
- [OK] Checkpoint run (timed POST):
  ```
  $ curl -i -X POST http://localhost:8000/reports -H "Content-Type: application/json" -d '{"topic":"cats"}'
  HTTP/1.1 202 Accepted
    date: Wed, 26 Aug 2026 08:22:28 GMT
    server: uvicorn
    content-length: 64
    content-type: application/json

    {"id":"20ada31b-3824-4c77-9b7a-cf749a8d716f","status":"pending"}

  ```
- [ ] Checkpoint run (poll ~10s later):
  ```
  $ curl -i http://localhost:8000/reports/<id>
    HTTP/1.1 200 OK
    date: Wed, 26 Aug 2026 08:57:57 GMT
    server: uvicorn
    content-length: 137
    content-type: application/json

    {"id":"3c6a9feb-e341-48e0-bb17-85351ec959e9","topic":"cats","status":"done","result":"Report on 'cats': here are 3 interesting facts..."}
  ```
- [OK] Committed: `Stage 2: 202 + background job + status endpoint`

Notes:


---

## Stage 3 — Jobs fail. Watch the retry.
**Goal:** `topic: "fail"` triggers 3 attempts (retries: 2), ends Failed; bad input is 400, no job

- [OK] `build-report` throws when `topic === "fail"`
- [OK] Function config: `retries: 2`
- [OK] Dashboard shows: attempt 1 fail → wait → attempt 2 → attempt 3 → **Failed**
  - Screenshot / notes:
- [OK] `POST /reports` with no `topic` → `400`, no event sent
  ```
  $ curl -i -X POST http://localhost:8000/reports -H "Content-Type: application/json" -d '{}'
  HTTP/1.1 400 Bad Request
    date: Wed, 26 Aug 2026 10:04:58 GMT
    server: uvicorn
    content-length: 30
    content-type: application/json

    {"detail":"topic is required"}
  ```
- [OK] README sentence written: *why retries ≠ validation*
  > retries are given to bad moments that could be server's fault (network fault, computation fault, etc) while bad input doesnt count as server's fault so calling error is fine.
- [OK] Committed: `Stage 3: retries seen, bad input rejected`

Notes:

---

## Stage 4 — The clock knocks: your first cron job
**Goal:** `heartbeat` function runs every minute on a cron trigger, logs pending/done/failed counts

- [OK] `heartbeat` function created with schedule `* * * * *`
- [OK] Logs one summary line per run (pending / done / failed counts)
- [OK] Dashboard shows ≥2 `heartbeat` runs, 1 minute apart
  - Screenshot / notes:

 ▕  Heartbeat: pending=0, done=0, failed=0
 ▕  127.0.0.1:49856 - "POST /api/inngest?fnId=report-api-heartbeat&stepId=step HTTP/1.1" 200
 ▕  127.0.0.1:49859 - "PUT /api/inngest HTTP/1.1" 200
 ▕  127.0.0.1:51876 - "PUT /api/inngest HTTP/1.1" 200
 ▕  127.0.0.1:51878 - "PUT /api/inngest HTTP/1.1" 200
 ▕  127.0.0.1:51881 - "PUT /api/inngest HTTP/1.1" 200
 ▕  127.0.0.1:51887 - "PUT /api/inngest HTTP/1.1" 200
 ▕  127.0.0.1:51890 - "PUT /api/inngest HTTP/1.1" 200
 ▕  127.0.0.1:51893 - "PUT /api/inngest HTTP/1.1" 200
 ▕  127.0.0.1:51899 - "PUT /api/inngest HTTP/1.1" 200
 ▕  127.0.0.1:51902 - "PUT /api/inngest HTTP/1.1" 200
 ▕  127.0.0.1:51905 - "PUT /api/inngest HTTP/1.1" 200
 ▕  127.0.0.1:51910 - "PUT /api/inngest HTTP/1.1" 200
 ▕  127.0.0.1:51918 - "PUT /api/inngest HTTP/1.1" 200
 ▕  Heartbeat: pending=0, done=0, failed=0
 ▕  127.0.0.1:51920 - "POST /api/inngest?fnId=report-api-heartbeat&stepId=step HTTP/1.1" 200

- [OK] README sentences written:
  - Cron for "every day at 08:00": `[expression]`
  - Cron for "every Sunday at 22:00": `[expression]`
- [OK] Committed: `Stage 4: cron heartbeat`

Notes:

---

## Stage 5 — Publish to GitHub
**Goal:** public repo + README a stranger can run in <5 min

- [OK] Repo is public: `[link]`
- [OK] README includes:
  - [OK] What this is
  - [OK] How to run (2 commands: API + Dev Server)
  - [OK] Endpoint/function table
  - [OK] Pasted 202 + poll proof
  - [OK] Stage 3 sentence
  - [OK] Stage 4 sentences
  - [OK] Dashboard screenshot
- [OK] Committed: `Stage 5: publish and docs`

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