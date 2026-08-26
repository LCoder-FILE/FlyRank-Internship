from fastapi import FastAPI

import logging
import datetime
import inngest
import inngest.fast_api


# Server setup 

app = FastAPI()

inngest_client = inngest.Inngest(
    app_id="report-api",
    logger=logging.getLogger("uvicorn"),
    is_production=False,
)



# Helper function

@inngest_client.create_function(
    fn_id="say-hello",
    trigger=inngest.TriggerEvent(event="test/hello"),
)
async def say_hello(ctx: inngest.Context) -> str:
    await ctx.step.sleep("wait-5s", datetime.timedelta(seconds=5))
    return "Hello from the background!"



# GET Function

@app.get("/health")
def get_health():
    return { "status": "ok" } 


inngest.fast_api.serve(app, inngest_client, [say_hello])

# to current dir (from FlyRank-Internship) : cd "Backend AI Track/Week 7/Your first background job"
# to run : fastapi dev server.py (terminal 1)  +  npx inngest-cli@latest dev -u http://localhost:8000/api/inngest (terminal 2)