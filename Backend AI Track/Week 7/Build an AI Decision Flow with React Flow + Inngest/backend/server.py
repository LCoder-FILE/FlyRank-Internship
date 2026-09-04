import os
import logging
from dotenv import load_dotenv
import uuid
import inngest
import inngest.fast_api

load_dotenv()

from fastapi import FastAPI
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

run_results: dict[str, dict] = {}

class RunRequest(BaseModel):
    graph: dict
    startNodeId: str


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


@inngest_client.create_function(
    fn_id="run-workflow",
    trigger=inngest.TriggerEvent(event="workflow/run"),
)
async def run_workflow(ctx: inngest.Context):
    graph = ctx.event.data["graph"]
    current_id = ctx.event.data["startNodeId"]
    run_id = ctx.event.data["runId"]
    history = []

    try:
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

            decision = await ctx.step.run(f"decide-{current_id}", ask_llm)
            history.append({"nodeId": current_id, "prompt": node["data"]["prompt"], "decision": decision})
            run_results[run_id] = {"status": "running", "history": history}

            next_edge = next(
                (e for e in graph["edges"]
                 if e["source"] == current_id and e["sourceHandle"] == decision.lower()),
                None,
            )
            current_id = next_edge["target"] if next_edge else None

        run_results[run_id] = {"status": "completed", "history": history}
    except Exception as e:
        run_results[run_id] = {"status": "failed", "history": history, "error": str(e)}
        raise

    return {"history": history}


# --- Routes ---
@app.get("/health")
def get_health():
    return {"status": "ok"}


@app.get("/api/workflows/run/{run_id}")
def get_run(run_id: str):
    return run_results.get(run_id, {"status": "not_found"})


@app.post("/api/workflows/run")
async def trigger_run(req: RunRequest):
    run_id = str(uuid.uuid4())
    run_results[run_id] = {"status": "running", "history": []}
    await inngest_client.send(
        inngest.Event(
            name="workflow/run",
            data={"graph": req.graph, "startNodeId": req.startNodeId, "runId": run_id},
        )
    )
    return {"runId": run_id}


inngest.fast_api.serve(app, inngest_client, [run_workflow])