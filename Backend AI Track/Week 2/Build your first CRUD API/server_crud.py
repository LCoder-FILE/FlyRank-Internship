from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] } # API description

@app.get("/health")
async def health():
    return { "status": "ok" }


# to run : uvicorn server_crud:app --reload --port 8000 (make sure in ./Backend AI Track/Week 2/Build your first CRUD API/)
# to run : fastapi dev server_crud.py (use this one)

