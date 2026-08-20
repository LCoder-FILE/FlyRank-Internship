import os
import time
import random
import json

from dotenv import load_dotenv
from openai import OpenAI, APITimeoutError, APIStatusError


load_dotenv()

client = OpenAI(
    base_url=os.environ["LLM_BASE_URL"],
    api_key=os.environ["LLM_API_KEY"],
    timeout=30.0,
    max_retries=0,   # we'll write our own retry policy in Stage 4
)


def load_prompt(path: str) -> str:
    with open(path) as f:
        return f.read()


def call_model(title: str) -> tuple[str, dict]:
    system_prompt = load_prompt("prompts/normalize-v1.md")
    start = time.time()

    res = call_with_retry(lambda: client.chat.completions.create(
        model=os.environ["LLM_MODEL"],
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": title},
        ],
    ))

    duration_ms = int((time.time() - start) * 1000)
    log_line = {
        "prompt_version": "v1",
        "model": os.environ["LLM_MODEL"],
        "input_tokens": getattr(res.usage, "prompt_tokens", None),
        "output_tokens": getattr(res.usage, "completion_tokens", None),
        "duration_ms": duration_ms,
        "repaired": False,
    }
    print(json.dumps(log_line))
    return res.choices[0].message.content, log_line

    


def call_with_retry(fn, max_attempts=3):
    error_status_code = [429, 500, 502, 503, 504]
    for attempt in range(max_attempts):
        try:
            return fn()
        except APITimeoutError:
            if attempt == max_attempts - 1:
                raise
        except APIStatusError as se:
            if se.status_code not in error_status_code:
                raise
            if attempt == max_attempts -1:
                raise

        time.sleep((2*attempt) + random.uniform(0,0.5))


if __name__ == "__main__":
    res = client.chat.completions.create(
        model=os.environ["LLM_MODEL"],
        messages=[{"role": "user", "content": "Reply with exactly the word: ready"}],
    )
    print(res.choices[0].message.content)

