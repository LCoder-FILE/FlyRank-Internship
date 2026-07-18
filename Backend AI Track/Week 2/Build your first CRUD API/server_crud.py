from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional


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




# PUT functions

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

@app.put("/tasks/{id}")
async def update_task(id: int, update: TaskUpdate):
    target_task = None
    for task in task_list:
        if task["id"] == id:
            target_task = task
            break

    if target_task == None:
        return JSONResponse(status_code=404, content={"error" : f"Task {id} not found"})
    
    if update.title == None and update.done == None:
        return JSONResponse(status_code=400, content={"error": f"No update provided"})

    if update.title != None and update.title.strip() == "":
        return JSONResponse(status_code=404, content={"error": "Title cannot be empty"})
    

    if update.title != None:
        target_task["title"] = update.title
    if update.done != None:
        target_task["done"] = update.done

    return target_task



# DELETE functions

@app.delete("/tasks/{id}")
async def delete_task(id: int):
    for task in task_list:
        if task["id"] == id:
            task_list.remove(task)
            return JSONResponse(status_code=204, content={"message": f"Task {id} successfully removed"})

    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})



# to run : fastapi dev server_crud.py (use this one & make sure in ./Backend AI Track/Week 2/Build your first CRUD API/)

