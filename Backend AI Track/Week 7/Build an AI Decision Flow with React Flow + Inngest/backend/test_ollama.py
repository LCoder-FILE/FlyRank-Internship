from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

response = client.chat.completions.create(
    model="gemma3:1b",
    messages=[{"role": "user", "content": "Is this a support request? Answer only YES or NO."}],
)
print(response.choices[0].message.content)