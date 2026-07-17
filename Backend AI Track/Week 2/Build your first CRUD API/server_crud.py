from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "Hello world !!!"} # use json as the main communication object.

# to run : uvicorn server_crud:app --reload --port 8000 (make sure in ./Backend AI Track/Week 2/Build your first CRUD API/)
# to run : fastapi dev server_crud.py

