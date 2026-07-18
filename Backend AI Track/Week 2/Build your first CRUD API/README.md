# Task API — CRUD Checkpoint

A minimal FastAPI CRUD API for managing tasks. Built as part of the Week 2 "Build your first CRUD API" exercise.

## Run Instructions

```bash
# 1. Install dependencies
pip install "fastapi[standard]"

# 2. Navigate to the project folder
cd "./Backend AI Track/Week 2/Build your first CRUD API/"

# 3. Start the dev server
fastapi dev server_crud.py
```

Server runs at `http://127.0.0.1:8000`. Interactive Swagger docs are available at `http://127.0.0.1:8000/docs`.

## Endpoints

| Method | Path          | Description                          | Success | Error(s)             |
|--------|---------------|---------------------------------------|---------|-----------------------|
| GET    | `/`           | API info (name, version, endpoints)  | 200     | —                     |
| GET    | `/health`     | Health check                          | 200     | —                     |
| GET    | `/tasks`      | List all tasks                        | 200     | —                     |
| GET    | `/tasks/{id}` | Get one task by id                    | 200     | 404 (id not found)    |
| POST   | `/tasks`      | Create a new task                     | 201     | 400 (missing/empty title) |
| PUT    | `/tasks/{id}` | Update a task's title and/or done     | 200     | 404, 400 (empty/invalid body) |
| DELETE | `/tasks/{id}` | Delete a task                         | 204     | 404 (id not found)    |

## Checkpoint — Full CRUD via curl

Example: create → update → confirm.

```cmd
(fenv-flyrank) D:\...\Build your first CRUD API>curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Go Exercise\"}"
HTTP/1.1 201 Created
date: Sat, 18 Jul 2026 13:04:30 GMT
server: uvicorn
content-length: 43
content-type: application/json

{"id":4,"title":"Go Exercise","done":false}
```

The rest of the CRUD lifecycle (update title, mark done, delete, and confirm with `GET /tasks`) was verified end-to-end, hitting every required status code: `201`, `200`, `204`, `404`, `400`.

## Swagger UI

Screenshots of each operation group, tried out live in `/docs`:

**Create**
![Create](./screenshot/Stage%205%20-%20Swagger%20UI/Create.png)

**Read**
![Read](./screenshot/Stage%205%20-%20Swagger%20UI/Read.png)

**Update**
![Update](./screenshot/Stage%205%20-%20Swagger%20UI/Update.png)

**Delete**
![Delete](./screenshot/Stage%205%20-%20Swagger%20UI/Delete.png)

## Repository

```bash
git clone https://github.com/LCoder-FILE/FlyRank-Internship
```
See: `FlyRank-Internship/Backend AI Track/Week 2/Build your first CRUD API`