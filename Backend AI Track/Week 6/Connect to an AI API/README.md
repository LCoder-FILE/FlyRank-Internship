# Put an LLM behind your API — /normalize

FlyRank Internship · Backend AI Track · Week 7 · A17

## What this does

Takes a messy job title string (e.g. "Sr. SWE II", "Senior Software Eng.") and returns
a single canonical title from a fixed list, with a confidence score. One request in,
one structured JSON answer out — no conversation, no memory.

## Quickstart

```bash
# 1. Clone and install
pip install -r requirements.txt

# 2. Copy env template and fill in your values
cp .env.example .env

# 3. Start Ollama (see Provider section below)
ollama serve

# 4. Run the API
fastapi dev server.py
```

**Try it:**
```bash
curl -X POST http://localhost:8000/normalize \
  -H "Content-Type: application/json" \
  -d '{"title": "Sr. SWE II"}'
```
Expected response:
```json
[PASTE YOUR REAL RESPONSE HERE ONCE STAGE 1/3 IS WORKING]
```

## Job card

See [`JOB-CARD.md`](./JOB-CARD.md) for the full input/output contract, closed lists,
and "must never" rules.

## Provider

- **Provider:** Ollama (local)
- **Model:** `gemma3:1b`
- **Env vars needed:** `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`
- Note: this machine's NVIDIA driver (12.7) is incompatible with Ollama's CUDA build,
  so inference runs on CPU (`CUDA_VISIBLE_DEVICES=cpu`) rather than GPU.

Swapping to a different provider (e.g. OpenRouter) only requires changing these three
`.env` values — nothing else in the code changes. That's the whole point of routing
every provider through the same OpenAI-compatible client.

## Stage log

### Stage 0 — Provider setup 

Confirmed a working round-trip to the model from `llm/client.py`. The only difference
between running a model on my laptop vs. a datacenter is three environment variables
(`LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`) — nothing else in the code changes.

### Stage 1 — Endpoint, validation, stub mode

Server running and connected to Supabase
 ▕  Application startup complete.
LLM_STUB = 1
 ▕  127.0.0.1:62977 - "POST /normalize HTTP/1.1" 200
LLM_STUB = 1
 ▕  127.0.0.1:62989 - "POST /normalize HTTP/1.1" 200
 ▕  127.0.0.1:62994 - "POST /normalize HTTP/1.1" 422

(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship\Backend AI Track\Week 6\Connect to an AI API>set LLM_STUB=1&& fastapi dev server.py
(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship\Backend AI Track\Week 6\Connect to an AI API>curl -X POST http://127.0.0.1:8000/normalize -H "Content-Type: application/json" -d "{\"title\": \"Sr. SWE II\"}"
{"canonical_title":"software_engineer","confidence":0.99,"original":"Sr. SWE II"}
(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship\Backend AI Track\Week 6\Connect to an AI API>curl -X POST http://localhost:8000/normalize -H "Content-Type: application/json" -d "{\"title\": \"\"}"
{"detail":[{"type":"string_too_short","loc":["body","title"],"msg":"String should have at least 1 character","input":"","ctx":{"min_length":1} }]}

### Stage 2 — Prompt as a versioned spec

set LLM_STUB=0&& fastapi dev server.py

Server running and connected to Supabase
 ▕  Application startup complete.
 ▕  127.0.0.1:53096 - "POST /normalize HTTP/1.1" 200
 ▕  127.0.0.1:53132 - "POST /normalize HTTP/1.1" 200
 ▕  127.0.0.1:53142 - "POST /normalize HTTP/1.1" 200

(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship\Backend AI Track\Week 6\Connect to an AI API>curl -X POST http://localhost:8000/normalize -H "Content-Type: application/json" -d "{\"title\": \"Sr. SWE II\"}"   
{"raw":"```json\n{\n  \"canonical_title\": \"senior_software_engineer\",\n  \"confidence\": 0.9\n}\n```"}
(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship\Backend AI Track\Week 6\Connect to an AI API>curl -X POST http://localhost:8000/normalize -H "Content-Type: application/json" -d "{\"title\": \"Product Owner\"}"
{"raw":"```json\n{\n  \"canonical_title\": \"product_owner\",\n  \"confidence\": 0.95\n}\n```"}
(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship\Backend AI Track\Week 6\Connect to an AI API>curl -X POST http://localhost:8000/normalize -H "Content-Type: application/json" -d "{\"title\": \"Chief Happiness Officer\"}"
{"raw":"{\"canonical_title\": \"other\", \"confidence\": 0.2}"}

### Stage 3 — Parse, validate, repair, quarantine

Tried forcing a validation failure via prompt override; gemma3:1b resisted even a first-position, repeated, explicit contradictory instruction — it stuck to its trained categories. A real failure was instead observed naturally on 'Product Owner', which the model got wrong even after one repair retry; this correctly triggered a 422 and a quarantine log entry (see logs/quarantine.jsonl)."

(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship>curl -X POST http://localhost:8000/normalize -H "Content-Type: application/json" -d "{\"title\": \"Sr. SWE II\"}"
{"canonical_title":"senior_software_engineer","confidence":0.95,"original":"Sr. SWE II"}
(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship>curl -X POST http://localhost:8000/normalize -H "Content-Type: application/json" -d "{\"title\": \"Product Owner\"}"
{"error":"model could not produce a valid result"}


### Stage 4 — Timeout, retries, cost logging, kill switch

set LLM_ENABLED=true
fastapi dev server.py

(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship>curl -X POST http://localhost:8000/normalize -H "Content-Type: application/json" -d "{\"title\": \"Sr. SWE II\"}"
{"canonical_title":"senior_software_engineer","confidence":0.9,"original":"Sr. SWE II"}

set LLM_ENABLED=false
fastapi dev server.py

(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship>curl -X POST http://localhost:8000/normalize -H "Content-Type: application/json" -d "{\"title\": \"Sr. SWE II\"}"
{"error":"LLM feature disabled"}

set LLM_BASE_URL=http://localhost:9999/v1/
fastapi dev server.py

(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship>curl -X POST http://localhost:8000/normalize -H "Content-Type: application/json" -d "{\"title\": \"Sr. SWE II\"}"
Internal Server Error

set LLM_BASE_URL=http://localhost:11434/v1/
fastapi dev server.py

(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship>curl -X POST http://localhost:8000/normalize -H "Content-Type: application/json" -d "{\"title\": \"Sr. SWE II\"}"
{"canonical_title":"senior_software_engineer","confidence":0.9,"original":"Sr. SWE II"}

 ▕  Will watch for changes in these directories: ['D:\\6.5th Semester CIT\\flyrank\\FlyRank-Internship\\Backend AI Track\\Week 6\\Connect to an AI API']
 ▕  Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
 ▕  Started reloader process [22916] using WatchFiles
 ▕  Started server process [34948]
 ▕  Waiting for application startup.
Server running and connected to Supabase
 ▕  Application startup complete.
{"prompt_version": "v1", "model": "gemma3:1b", "input_tokens": 251, "output_tokens": 32, "duration_ms": 4362, "repaired": false}
 ▕  127.0.0.1:63161 - "POST /normalize HTTP/1.1" 200


### Stage 5 — Eval results
[FILL IN: score, date, prompt version, e.g. "6/8 (75%) — 2026-08-25 — prompt v1"]

## What I'd fix with another day

[FILL IN once you're at Stage 5]

## AI vs me (bonus stage, if attempted)

[FILL IN if you do the bonus stage]