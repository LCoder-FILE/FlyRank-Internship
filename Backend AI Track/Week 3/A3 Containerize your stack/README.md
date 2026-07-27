# Task API

A small FastAPI + PostgreSQL task manager, containerized with Docker Compose.
On startup, the app connects to Postgres, creates the `tasks` table if it
doesn't exist, and seeds 3 example tasks the first time it runs.

## Run everything

```bash
docker compose up
```

This starts both the API (`http://localhost:8000`) and the Postgres database
in one command — no local Python or Postgres install required.

Interactive API docs: `http://localhost:8000/docs`

## Environment variables

Copy the example file and adjust if needed:

```bash
cp .env.example .env
```

| Variable       | Description                              | Example                                         |
|----------------|-------------------------------------------|--------------------------------------------------|
| `DATABASE_URL` | Postgres connection string                | `postgresql://postgres:dev@localhost:5432/tasks` |

See [`.env.example`](./.env.example) for the full template.

> Note: when running via `docker compose up`, the API container talks to the
> `db` service over Docker's internal network, so `DATABASE_URL` inside
> `compose.yaml` uses `db` as the hostname instead of `localhost`.

## Endpoints

| Method | Path          | Description                     |
|--------|---------------|----------------------------------|
| GET    | `/`           | API info                        |
| GET    | `/health`     | Health check                    |
| GET    | `/tasks`      | List all tasks                  |
| GET    | `/tasks/{id}` | Get a single task by id          |
| POST   | `/tasks`      | Create a new task                |
| PUT    | `/tasks/{id}` | Update a task's title and/or done status |
| DELETE | `/tasks/{id}` | Delete a task by id              |

## Example request

```bash
curl -i http://127.0.0.1:8000/tasks
```

```
HTTP/1.1 200 OK
content-type: application/json

[[1,"Wake up early",true],[2,"Cook breakfast",false],[3,"Make a cup of coffee",false]]
```

## Verifying data in the database

Connect to the running Postgres container and inspect the table directly:

```bash
docker exec -it taskdb psql -U postgres -d tasks -c "\dt"
docker exec -it taskdb psql -U postgres -d tasks -c "SELECT * FROM tasks;"
```

Or use a free GUI client (DBeaver, pgAdmin, TablePlus) with:
- Host: `localhost`
- Port: `5432`
- Database: `tasks`
- User: `postgres`
- Password: `dev`

**Screenshot:**

<!--
Paste a screenshot here showing:
  1. `\dt` output listing the `tasks` table
  2. A `SELECT * FROM tasks;` result with the seeded/created rows
-->

![Database contents](./screenshot/db-tasks.png)

## Project history / stage log

See [`README.Docker.md`](./README.Docker.md) for the full step-by-step build
log (Postgres setup, `.gitignore`, `.env`, CRUD implementation, and
Dockerization stages).