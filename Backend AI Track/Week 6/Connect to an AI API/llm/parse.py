import json
import os
import re
import time

from pydantic import ValidationError
from llm.schema import NormalizeOutput
from llm.client import call_model, load_prompt, client, call_with_retry


def extract_json(text: str) -> dict:
    """Strip code fences / extra text, find the JSON object, parse it."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("no JSON object found in model output")
    return json.loads(match.group(0))


def get_normalized(title: str) -> tuple[NormalizeOutput | None, str | None]:
    raw, log_line = call_model(title)

    try:
        data = extract_json(raw)
        data["original"] = title
        return NormalizeOutput(**data), None
    except (ValueError, ValidationError, json.JSONDecodeError) as e:
        first_error = str(e)


    system_prompt = load_prompt("prompts/normalize-v1.md")
    repair_msg = (
        f"Your previous answer was rejected for this reason: {first_error}\n"
        f"Previous answer: {raw}\n"
        "Return only corrected JSON matching the schema."
    )
    start = time.time()
    res = call_with_retry(lambda: client.chat.completions.create(
        model=os.environ["LLM_MODEL"],
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": title},
            {"role": "assistant", "content": raw},
            {"role": "user", "content": repair_msg},
        ],
    ))
    duration_ms = int((time.time() - start) * 1000)
    print(json.dumps({
        "prompt_version": "v1",
        "model": os.environ["LLM_MODEL"],
        "input_tokens": getattr(res.usage, "prompt_tokens", None),
        "output_tokens": getattr(res.usage, "completion_tokens", None),
        "duration_ms": duration_ms,
        "repaired": True,
    }))
    raw2 = res.choices[0].message.content

    try:
        data = extract_json(raw2)
        data["original"] = title
        return NormalizeOutput(**data), None
    except (ValueError, ValidationError, json.JSONDecodeError) as e:
        return None, f"raw_output={raw2!r} error={e}"
