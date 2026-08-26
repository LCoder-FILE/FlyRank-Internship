from fastapi import FastAPI

app = FastAPI()

# GET Functions

@app.get("/health")
def get_health():
    return { "status": "ok" } 



# to run : fastapi dev server.py