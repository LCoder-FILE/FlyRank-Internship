from fastapi import FastAPI, HTTPException


task_list = [
    {"id": 1, "title": "cook", "done":False},
    {"id": 2, "title": "laundry", "done":True},
    {"id": 3, "title": "study", "done":False}
]

app = FastAPI()

@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] } # API description

@app.get("/health")
async def health():
    return { "status": "ok" }

@app.get("/tasks")
async def tasks():
    return task_list

@app.get("/tasks/{id}")
async def get_task(id: int):
    for task in task_list:
        if task["id"] == id:
            return task
        
    raise HTTPException(status_code=404, detail={ "error": f"Task {id} not found" })


# to run : fastapi dev server_crud.py (use this one & make sure in ./Backend AI Track/Week 2/Build your first CRUD API/)

