
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


## commit  

```cmd
Stage 0: Postgres in Docker + gitignore
```