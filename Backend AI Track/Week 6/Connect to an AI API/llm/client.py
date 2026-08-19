import os
from dotenv import load_dotenv
from openai import OpenAI

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

def call_model(title: str) -> str:
    system_prompt = load_prompt("prompts/normalize-v1.md")
    res = client.chat.completions.create(
        model=os.environ["LLM_MODEL"],
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": title},
        ],
    )
    return res.choices[0].message.content


if __name__ == "__main__":
    res = client.chat.completions.create(
        model=os.environ["LLM_MODEL"],
        messages=[{"role": "user", "content": "Reply with exactly the word: ready"}],
    )
    print(res.choices[0].message.content)

