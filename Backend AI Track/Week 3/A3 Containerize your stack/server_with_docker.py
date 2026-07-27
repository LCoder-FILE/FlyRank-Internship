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

# Setup db

create_tasks_table = """
    create table if not exists tasks(
        id integer primary key,
        title text not null,
        done integer not null default 0
    )
"""

count_exist_data = "select count(*) from tasks"

cur.execute(create_tasks_table)
cur.execute(count_exist_data)

count = cur.fetchone()[0]

if count == 0:
    example_tasks = [("Wake up", 1), ("Make a cup of coffee", 0), ("Eat breakfast", 0)]
    cur.executemany("insert into tasks (title, done) values (?, ?)", example_tasks)
    print("Done insertion 3 sample tasks (seeds)")

else:
    print(f"Exist {count} rows - skipping seed")

conn.commit()

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
    

    return JSONResponse(status_code=200, content={"message": f"Task {id} successfully removed"}) # tried 204 code but server return some error message (like the task not found)



# to run : fastapi dev server_with_docker.py (use this one & make sure in ./Backend AI Track/Week 3/A3 Containerize your stack/)



# Work documentation (checkpoint)







