import os
import logging
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
import inngest
import inngest.fast_api
from openai import OpenAI

# --- Setup ---
app = FastAPI()

inngest_client = inngest.Inngest(
    app_id="ai-workflow-builder",
    logger=logging.getLogger("uvicorn"),
    is_production=False,
)

llm_client = OpenAI(
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
    api_key=os.getenv("OLLAMA_API_KEY", "ollama"),
)
MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b")


# --- Inngest function ---
@inngest_client.create_function(
    fn_id="run-workflow",
    trigger=inngest.TriggerEvent(event="workflow/run"),
)
async def run_workflow(ctx: inngest.Context, step: inngest.Step):
    graph = ctx.event.data["graph"]        # {"nodes": {...}, "edges": [...]}
    current_id = ctx.event.data["startNodeId"]
    history = []

    while current_id:
        node = graph["nodes"][current_id]

        async def ask_llm(prompt=node["data"]["prompt"]):
            resp = llm_client.chat.completions.create(
                model=MODEL,
                messages=[{
                    "role": "user",
                    "content": f"{prompt}\n\nAnswer with exactly one word: YES or NO.",
                }],
                temperature=0,
            )
            answer = resp.choices[0].message.content.strip().upper()
            return "YES" if "YES" in answer else "NO"

        decision = await step.run(f"decide-{current_id}", ask_llm)
        history.append({"nodeId": current_id, "prompt": node["data"]["prompt"], "decision": decision})

        next_edge = next(
            (e for e in graph["edges"]
             if e["source"] == current_id and e["sourceHandle"] == decision.lower()),
            None,
        )
        current_id = next_edge["target"] if next_edge else None

    return {"history": history}


# --- Routes ---
@app.get("/health")
def get_health():
    return {"status": "ok"}


inngest.fast_api.serve(app, inngest_client, [run_workflow])