import logging
import datetime
import inngest
import inngest.fast_api
import uuid

from fastapi import HTTPException
from pydantic import BaseModel
from fastapi import FastAPI


# In memory storage

reports: dict[str, dict] = {}

class ReportRequest(BaseModel):
    topic: str | None = None


# Server setup 

app = FastAPI()

inngest_client = inngest.Inngest(
    app_id="report-api",
    logger=logging.getLogger("uvicorn"),
    is_production=False,
)


# Helper Functions

@inngest_client.create_function(
    fn_id="say-hello",
    trigger=inngest.TriggerEvent(event="test/hello"),
)
async def say_hello(ctx: inngest.Context) -> str:
    await ctx.step.sleep("wait-5s", datetime.timedelta(seconds=5))
    return "Hello from the background!"


@inngest_client.create_function(
    fn_id="make-report",
    trigger=inngest.TriggerEvent(event="report/requested"),
    retries=2,
)
async def make_report(ctx: inngest.Context) -> None:
    report_id = ctx.event.data["id"]
    topic = ctx.event.data["topic"]

    await ctx.step.sleep("do-the-slow-work", datetime.timedelta(seconds=8))

    async def _build_report():
        if topic == "fail":
            raise Exception("The report oven is broken!")
        result = f"Report on '{topic}': here are 3 interesting facts..."
        reports[report_id]["status"] = "done"
        reports[report_id]["result"] = result
        return result

    await ctx.step.run("build-report", _build_report)


@inngest_client.create_function(
    fn_id="heartbeat",
    trigger=inngest.TriggerCron(cron="* * * * *"),
)
async def heartbeat(ctx: inngest.Context) -> None:
    pending = sum(1 for r in reports.values() if r["status"] == "pending")
    done = sum(1 for r in reports.values() if r["status"] == "done")
    failed = sum(1 for r in reports.values() if r["status"] == "failed")
    ctx.logger.info(f"Heartbeat: pending={pending}, done={done}, failed={failed}")


# GET Functions

@app.get("/health")
def get_health():
    return { "status": "ok" } 

@app.get("/reports/{report_id}")
def get_report(report_id:str):
    report = reports.get(report_id)
    if report == None:
        raise HTTPException(status_code=404, detail="report not found")

    return report



# POST Functions

@app.post("/reports", status_code=202)
async def create_report(body: ReportRequest):
    if not body.topic:
        raise HTTPException(status_code=400, detail="topic is required")

    report_id = str(uuid.uuid4())
    reports[report_id] = {
        "id": report_id,
        "topic": body.topic,
        "status": "pending",
    }

    await inngest_client.send(
        inngest.Event(
            name="report/requested",
            data={"id": report_id, "topic": body.topic},
        )
    )

    return {"id": report_id, "status": "pending"}



inngest.fast_api.serve(app, inngest_client, [say_hello, make_report, heartbeat])

# to current dir (from FlyRank-Internship) : cd "Backend AI Track/Week 7/Your first background job"
# to run : fastapi dev server.py (terminal 1)  +  npx inngest-cli@latest dev -u http://localhost:8000/api/inngest (terminal 2)

"""
time curl -i -X POST http://localhost:8000/reports -H "Content-Type: application/json" -d '{"topic":"cats"}'
"""