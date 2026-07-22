from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

import sqlite3


# task_list = [
#     {"id": 1, "title": "cook", "done":False},
#     {"id": 2, "title": "laundry", "done":True},
#     {"id": 3, "title": "study", "done":False}
# ]

app = FastAPI()
db_file = "tasks.db" # because we on ./Backend AI Track/Week 3/A2 Connecting to the database/

conn = sqlite3.connect(db_file)
cur = conn.cursor()

# GET functions

@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] } # API description

@app.get("/health")
async def health():
    return { "status": "ok" }

@app.get("/tasks")
async def tasks():
    get_tasks_query = "SELECT * FROM tasks"
    cur.execute(get_tasks_query)

    task_list = cur.fetchall()
    return task_list

@app.get("/tasks/{id}")
async def get_task(id: int):
    get_tasks_by_id_query = "SELECT * FROM tasks WHERE id = ?"
    cur.execute(get_tasks_by_id_query, (id, ))

    searched_task = cur.fetchone()
    if searched_task == None:
        raise HTTPException(status_code=404, detail={ "error": f"Task {id} not found" })
    else:
        return searched_task



# POST functions

class TaskCreate(BaseModel):
    title: str

@app.post("/tasks")
async def create_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        return JSONResponse(status_code=400, content={"message" : "Task's title is required"}) 

    add_task_query = "INSERT INTO tasks (title, done) VALUES (?, ?)"
    cur.execute(add_task_query, (task.title, 0))

    conn.commit()

    new_task = {
        "id" : cur.lastrowid,
        "title" : task.title,
        "done" : False
    }
    return JSONResponse(status_code=201, content=new_task)




# PUT functions

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

@app.put("/tasks/{id}")
async def update_task(id: int, update: TaskUpdate):
    update_task_query = "UPDATE tasks SET title = ?, done = ? WHERE id = ?"
    get_tasks_by_id_query = "SELECT * FROM tasks WHERE id = ?"

    cur.execute(get_tasks_by_id_query, (id, ))
    searched_task = cur.fetchone()
    if searched_task == None:
        raise HTTPException(status_code=404, detail={ "error": f"Task {id} not found" })
    
    if update.title == None and update.done == None:
        return JSONResponse(status_code=400, content={"error": f"No update provided"})

    if update.title != None and update.title.strip() == "":
        return JSONResponse(status_code=404, content={"error": "Title cannot be empty"})

    cur.execute(update_task_query, (update.title, update.done, id))
    conn.commit()

    cur.execute(get_tasks_by_id_query, (id, ))
    updated_task = cur.fetchone()

    return updated_task



# DELETE functions

@app.delete("/tasks/{id}")
async def delete_task(id: int):
    delete_task_by_id_query = "DELETE FROM tasks WHERE id = ?"
    get_tasks_by_id_query = "SELECT * FROM tasks WHERE id = ?"
    
    cur.execute(get_tasks_by_id_query, (id, ))
    searched_task = cur.fetchone()
    if searched_task == None:
        raise HTTPException(status_code=404, detail={ "error": f"Task {id} not found" })

    cur.execute(delete_task_by_id_query, (id, ))
    conn.commit()
    

    return JSONResponse(status_code=200, content={"message": f"Task {id} successfully removed"})



# to run : fastapi dev server_with_db.py (use this one & make sure in ./Backend AI Track/Week 3/A2 Connecting to the database/)



# Work documentation (checkpoint)

"""
Stage 1 : 

curl -i http://127.0.0.1:8000/tasks -> HTTP/1.1 200 OK + [[1,"Wake up",1],[2,"Make a cup of coffee",0],[3,"Eat breakfast",0]]
curl -i http://127.0.0.1:8000/tasks/2 -> HTTP/1.1 200 OK + [2,"Make a cup of coffee",0]

curl -i http://127.0.0.1:8000/tasks/999 -> HTTP/1.1 404 Not Found + {"detail":{"error":"Task 999 not found"}}

commit : Stage 1: database read endpoints
"""


"""
Stage 2 : 

curl -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d "{\"title\": \"Go to school\"}" -> {"id":4,"title":"Go to school","done":false}
curl -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d "{\"title\": \"Exercise\"}" -> {"id":5,"title":"Exercise","done":false}

-- reload the app (ctrl + C -> fastapi dev server_with_db.py) --

curl -i http://127.0.0.1:8000/tasks -> HTTP/1.1 200 OK + [[1,"Wake up",1],[2,"Make a cup of coffee",0],[3,"Eat breakfast",0]],[4,"Go to school",0],[5,"Exercise",0]]

commit : Stage 2: insert into database
"""


"""
Stage 3 : 

curl -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d "{\"title\": \"Do Homework\"}" -> {"id":6,"title":"Do Homework","done":false}
curl -i http://127.0.0.1:8000/tasks -> HTTP/1.1 200 OK + [[1,"Wake up",1],[2,"Make a cup of coffee",0],[3,"Eat breakfast",0],[4,"Go to school",0],[5,"Exercise",0],[6,"Do Homework",0]]

curl -X PUT http://127.0.0.1:8000/tasks/6 -H "Content-Type: application/json" -d "{\"title\": \"Do Homework\", \"done\": true}" -> [6,"Do Homework",1]
curl -i http://127.0.0.1:8000/tasks -> HTTP/1.1 200 OK + [[1,"Wake up",1],[2,"Make a cup of coffee",0],[3,"Eat breakfast",0],[4,"Go to school",0],[5,"Exercise",0],[6,"Do Homework",1]]

curl -i -X DELETE http://127.0.0.1:8000/tasks/6 -> HTTP/1.1 200 OK + {"message":"Task 6 successfully removed"}
curl -i http://127.0.0.1:8000/tasks -> HTTP/1.1 200 OK + [[1,"Wake up",1],[2,"Make a cup of coffee",0],[3,"Eat breakfast",0]],[4,"Go to school",0],[5,"Exercise",0]]


commit : Stage 3: update and delete with SQL
"""

