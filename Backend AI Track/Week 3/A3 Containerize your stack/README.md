
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

---

# Stage 2

## Checkpoints

```cmd
curl -i http://127.0.0.1:8000/tasks -> HTTP/1.1 200 OK + [[1,"Wake up early",true],[2,"Cook breakfast",false],[3,"Make a cup of coffee",false]]
curl -i http://127.0.0.1:8000/tasks/999 -> HTTP/1.1 404 Not Found + {"detail":{"error":"Task 999 not found"} }

```


## Commit 

```cmd
Stage 2: read from Postgres
```

---

# Stage 3

## Checkpoints

```cmd
curl -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d "{\"title\": \"Go to school\"}" -> {"id":4,"title":"Go to school","done":false}
curl -X PUT http://127.0.0.1:8000/tasks/4 -H "Content-Type: application/json" -d "{\"title\": \"Do Homework\", \"done\": true}" -> [4,"Do Homework",true]

curl -i http://127.0.0.1:8000/tasks -> [[1,"Wake up early",true],[2,"Cook breakfast",false],[3,"Make a cup of coffee",false],[4,"Do Homework",true]]

curl -i -X DELETE http://127.0.0.1:8000/tasks/4 -> HTTP/1.1 200 OK + {"message":"Task 4 successfully removed"}

curl -i http://127.0.0.1:8000/tasks -> HTTP/1.1 200 OK + [[1,"Wake up early",true],[2,"Cook breakfast",false],[3,"Make a cup of coffee",false]]

```


## Commit 

```cmd
Stage 3: full CRUD on Postgres
```

---

# Stage 4

## Checkpoints

```cmd
(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship\Backend AI Track\Week 3\A3 Containerize your stack>docker compose up
[+] up 3/3
 ✔ Network a3containerizeyourstack_default Created                                                                 0.1s
 ✔ Container a3containerizeyourstack-db-1  Created                                                                 0.1s
 ✔ Container a3containerizeyourstack-api-1 Created                                                                 0.1s
Attaching to api-1, db-1
db-1  | 
db-1  | PostgreSQL Database directory appears to contain a database; Skipping initialization
db-1  | 
db-1  | 2026-07-27 12:39:45.729 UTC [1] LOG:  starting PostgreSQL 18.4 (Debian 18.4-1.pgdg13+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit
db-1  | 2026-07-27 12:39:45.731 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
db-1  | 2026-07-27 12:39:45.731 UTC [1] LOG:  listening on IPv6 address "::", port 5432
db-1  | 2026-07-27 12:39:45.739 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
db-1  | 2026-07-27 12:39:45.758 UTC [32] LOG:  database system shutdown was interrupted; last known up at 2026-07-27 12:39:32 UTC
db-1  | 2026-07-27 12:39:45.966 UTC [32] LOG:  database system was not properly shut down; automatic recovery in progress
db-1  | 2026-07-27 12:39:45.970 UTC [32] LOG:  redo starts at 0/1BEF610
db-1  | 2026-07-27 12:39:45.971 UTC [32] LOG:  invalid record length at 0/1BEF718: expected at least 24, got 0
db-1  | 2026-07-27 12:39:45.971 UTC [32] LOG:  redo done at 0/1BEF6E0 system usage: CPU: user: 0.00 s, system: 0.00 s, elapsed: 0.00 s
db-1  | 2026-07-27 12:39:45.983 UTC [30] LOG:  checkpoint starting: end-of-recovery immediate wait
db-1  | 2026-07-27 12:39:46.058 UTC [30] LOG:  checkpoint complete: wrote 0 buffers (0.0%), wrote 3 SLRU buffers; 0 WAL file(s) added, 0 removed, 0 recycled; write=0.007 s, sync=0.003 s, total=0.082 s; sync files=2, longest=0.002 s, average=0.002 s; distance=0 kB, estimate=0 kB; lsn=0/1BEF718, redo lsn=0/1BEF718
db-1  | 2026-07-27 12:39:46.063 UTC [1] LOG:  database system is ready to accept connections
api-1  | Done insertion 3 sample tasks (seeds)
api-1  | INFO:     Started server process [1]
api-1  | INFO:     Waiting for application startup.
api-1  | INFO:     Application startup complete.
api-1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)



```


## Commit 

```cmd
Stage 4: docker-compose the whole stack
```