from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def get_health():
    return { "status": "ok" } 


# to current dir (from FlyRank-Internship) : cd "Backend AI Track/Week 7/Your first background job"
# to run : fastapi dev server.py