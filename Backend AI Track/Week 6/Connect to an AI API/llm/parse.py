import json
import os
import re
from pydantic import ValidationError
from llm.schema import NormalizeOutput
from llm.client import call_model, load_prompt, client


def extract_json(text: str) -> dict:
    """Strip code fences / extra text, find the JSON object, parse it."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("no JSON object found in model output")
    return json.loads(match.group(0))


def get_normalized(title: str) -> tuple[NormalizeOutput | None, str | None]:
    """Returns (result, None) on success, or (None, error_message) if both
    the original call and the repair retry fail."""
    raw = call_model(title)

    try:
        data = extract_json(raw)
        data["original"] = title
        return NormalizeOutput(**data), None
    except (ValueError, ValidationError, json.JSONDecodeError) as e:
        first_error = str(e)

    # --- repair retry: one shot only ---
    system_prompt = load_prompt("prompts/normalize-v1.md")
    repair_msg = (
        f"Your previous answer was rejected for this reason: {first_error}\n"
        f"Previous answer: {raw}\n"
        "Return only corrected JSON matching the schema."
    )
    res = client.chat.completions.create(
        model=os.environ["LLM_MODEL"],
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": title},
            {"role": "assistant", "content": raw},
            {"role": "user", "content": repair_msg},
        ],
    )
    raw2 = res.choices[0].message.content

    try:
        data = extract_json(raw2)
        data["original"] = title
        return NormalizeOutput(**data), None
    except (ValueError, ValidationError, json.JSONDecodeError) as e:
        return None, f"raw_output={raw2!r} error={e}"