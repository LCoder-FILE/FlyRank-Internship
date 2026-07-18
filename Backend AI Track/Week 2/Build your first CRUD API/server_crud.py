from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel


task_list = [
    {"id": 1, "title": "cook", "done":False},
    {"id": 2, "title": "laundry", "done":True},
    {"id": 3, "title": "study", "done":False}
]

app = FastAPI()

# GET functions

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



# POST functions

class TaskCreate(BaseModel):
    title: str

@app.post("/tasks")
async def create_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        return JSONResponse(status_code=400, content={"message" : "Task's title is required"}) 

    next_id = len(task_list) + 1
    new_task = {"id": next_id, "title": task.title, "done": False}
    task_list.append(new_task)
    return JSONResponse(status_code=201, content=new_task)



# to run : fastapi dev server_crud.py (use this one & make sure in ./Backend AI Track/Week 2/Build your first CRUD API/)

