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

### Stage 0 — Provider setup ✅
Confirmed a working round-trip to the model from `llm/client.py`. The only difference
between running a model on my laptop vs. a datacenter is three environment variables
(`LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`) — nothing else in the code changes.

### Stage 1 — Endpoint, validation, stub mode
[FILL IN: describe input validation rules, what LLM_STUB=1 returns, and paste both
curl examples — one valid (200) and one invalid (422/400, naming the bad field)]

### Stage 2 — Prompt as a versioned spec
[FILL IN: link to prompts/normalize-v1.md, note anything surprising from testing
3 real inputs]

### Stage 3 — Parse, validate, repair, quarantine
[FILL IN: confirm repair-retry works, note what a quarantined entry looks like]

### Stage 4 — Timeout, retries, cost logging, kill switch
[FILL IN: timeout value used, which errors are retried, one cost-log example line,
confirm LLM_ENABLED=false behavior]

### Stage 5 — Eval results
[FILL IN: score, date, prompt version, e.g. "6/8 (75%) — 2026-08-25 — prompt v1"]

## What I'd fix with another day

[FILL IN once you're at Stage 5]

## AI vs me (bonus stage, if attempted)

[FILL IN if you do the bonus stage]