# Put an LLM behind your API — /normalize

FlyRank Internship · Backend AI Track · Week 7 · A17

## What this does

Takes a messy job title string (e.g. "Sr. SWE II", "Senior Software Eng.", "senior dev")
and returns a single canonical title from a fixed list, with a confidence score.
One request in, one structured JSON answer out — no conversation, no memory of
previous requests.

## Quickstart

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy env template and fill in your values
cp .env.example .env

# 3. Start Ollama (see Provider section below for local-GPU caveats)
ollama serve

# 4. In a second terminal, run the API
fastapi dev server.py
```

**Try it:**
```bash
curl -X POST http://localhost:8000/normalize \
  -H "Content-Type: application/json" \
  -d '{"title": "Sr. SWE II"}'
```
**Real response:**
```json
{"canonical_title":"senior_software_engineer","confidence":0.9,"original":"Sr. SWE II"}
```

**Invalid input example** (empty title, rejected before any model call):
```bash
curl -X POST http://localhost:8000/normalize \
  -H "Content-Type: application/json" \
  -d '{"title": ""}'
```
```json
{"detail":[{"type":"string_too_short","loc":["body","title"],"msg":"String should have at least 1 character","input":"","ctx":{"min_length":1}}]}
```

## Job card

See [`JOB-CARD.md`](./JOB-CARD.md) for the full input/output contract, closed lists,
and "must never" rules.

## Provider

| | |
|---|---|
| Provider | Ollama (local) |
| Model | `gemma3:1b` |
| Env vars needed | `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL` |

Swapping providers (e.g. to OpenRouter) only requires changing these three `.env`
values — nothing else in the code changes, since everything goes through the same
OpenAI-compatible client.

**Local GPU note:** this machine's NVIDIA driver (12.7) is incompatible with
Ollama's bundled CUDA build, causing a crash during inference (`CUDA error: the
provided PTX was compiled with an unsupported toolchain`). Worked around by forcing
CPU-only inference:
```bash
set CUDA_VISIBLE_DEVICES=cpu
ollama serve
```

## Reliability

- **Timeout:** 30s, set explicitly on the client (SDK default is 10 minutes).
- **Retries:** on timeout, 429, and 5xx only — never on 400/401/403 — with
  exponential backoff + jitter, max 3 attempts. Verified: pointing at an
  unreachable URL fails fast with no retry spam.
- **Cost logging:** one structured JSON line per model call —
  `{"prompt_version": "v1", "model": "gemma3:1b", "input_tokens": 251, "output_tokens": 32, "duration_ms": 4362, "repaired": false}`
- **Kill switch:** `LLM_ENABLED=false` returns an immediate `503` with zero model
  calls. Verified.

## Trustworthy output

Model output is parsed, stripped of markdown code fences, and validated against
the schema before anything is returned. On validation failure, one repair retry is
attempted (the model is shown its own broken output plus the exact error). If that
also fails, the endpoint returns a `422` and logs the failure to
`logs/quarantine.jsonl` — raw model text is never returned to the caller.

**Real quarantine example:** the input "Product Owner" caused `gemma3:1b` to invent
an out-of-enum category (`product_owner`) on both the original call and the repair
retry — it appears to have a strong prior toward this as a "real" title. Correctly
resulted in a `422` and a logged entry instead of bad data reaching the caller.

I also tried forcing a validation failure by adding a contradictory instruction
("always output X") to the prompt — even a first-position, repeated, explicit
override was ignored by the model in favor of its few-shot examples and training
priors. Small models appear to weight examples/priors over blunt instructions.

## Eval results

**Score: 6/8 (75%)** — 2026-08-19 — prompt v1