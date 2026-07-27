
# Stage 0  

## Setup docker image for postgres

```cmd
docker run --name taskdb -e POSTGRES_PASSWORD=dev -e POSTGRES_DB=tasks -p 5432:5432 -v taskdata:/var/lib/postgresql/data -d postgres
```

error : Docker pulled postgres:latest, which is now Postgres 18+. 
Starting with version 18, the official image changed its expected directory structure — it no longer wants the volume mounted directly at /var/lib/postgresql/data. 
Instead it wants the volume mounted one level up, at /var/lib/postgresql, and it creates a version-specific subdirectory inside that itself.


## Fix

```cmd
docker rm -f taskdb
taskdb

docker volume rm taskdata
taskdata

docker run --name taskdb -e POSTGRES_PASSWORD=dev -e POSTGRES_DB=tasks -p 5432:5432 -v taskdata:/var/lib/postgresql -d postgres

docker ps
CONTAINER ID   IMAGE      COMMAND                  CREATED          STATUS          PORTS                                         NAMES
e10a4cbc0ab0   postgres   "docker-entrypoint.s…"   14 seconds ago   Up 13 seconds   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp   taskdb

docker exec -it taskdb psql -U postgres -d tasks
psql (18.4 (Debian 18.4-1.pgdg13+1))
Type "help" for help.

tasks=#
```

## .gitignore

```cmd
# Environment variables / secrets
.env

# Python cache
__pycache__/
*.pyc

# Editor
.vscode/

# OS junk
.DS_Store
Thumbs.db
```


## Commit  

```cmd
Stage 0: Postgres in Docker + gitignore
```

---

# Stage 1

## Add .env file

```cmd
type nul > .env
```

## PostgreSQL driver installation

```cmd
pip install "psycopg[binary]"

Installing collected packages: tzdata, psycopg-binary, psycopg
Successfully installed psycopg-3.3.4 psycopg-binary-3.3.4 tzdata-2026.3
```

## Replace SQLite with PostgreSQL

```cmd
fastapi dev server_with_docker.py

docker exec -it taskdb psql -U postgres -d tasks -c "\dt"
          List of tables
 Schema | Name  | Type  |  Owner   
--------+-------+-------+----------
 public | tasks | table | postgres
(1 row)

docker exec -it taskdb psql -U postgres -d tasks -c "SELECT * FROM tasks;"
 id |        title         | done 
----+----------------------+------
  1 | Wake up early        | t
  2 | Cook breakfast       | f
  3 | Make a cup of coffee | f
(3 rows)


 ⚡️ Starting FastAPI in development mode
Exist 3 rows - skipping seed
 
 🐍 Using import string: server_with_docker:app
 
 🌐 Server started at http://127.0.0.1:8000
    Documentation at http://127.0.0.1:8000/docs
 
  Logs:
 
 ▕  Will watch for changes in these directories: ['D:\\6.5th Semester CIT\\flyrank\\FlyRank-Internship\\Backend AI 
    Track\\Week 3\\A3 Containerize your stack']
 ▕  Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
 ▕  Started reloader process [26132] using WatchFiles
Exist 3 rows - skipping seed
 ▕  Started server process [7596]
 ▕  Waiting for application startup.
 ▕  Application startup complete.
 ▕  WatchFiles detected changes in 'server_with_docker.py'. Reloading...
 
 ▕  Shutting down
 ▕  Waiting for application shutdown.
 ▕  Application shutdown complete.
 ▕  Finished server process [7596]
Exist 3 rows - skipping seed
 ▕  Started server process [10212]
 ▕  Waiting for application startup.
 ▕  Application startup complete.
 ▕  WatchFiles detected changes in 'server_with_docker.py'. Reloading...
 
 ▕  Shutting down
 ▕  Waiting for application shutdown.
 ▕  Application shutdown complete.
 ▕  Finished server process [10212]
Exist 3 rows - skipping seed
 ▕  Started server process [24588]
 ▕  Waiting for application startup.
 ▕  Application startup complete.

```

## Commit  

```cmd
Stage 1: connect via .env and create table
```