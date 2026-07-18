
# Stage 0 - Hello, server

1. pip install "fastapi[standard]""
2. run the server_crud.py with : fastapi dev server_crud.py -> **use this one to run** & make sure in ./"Backend AI Track"/"Week 2"/"Build your first CRUD API"/
3. see the page with : curl -i http://127.0.0.1:8000/docs


# Stage 1 - Root and health endpoints

1. create two json endpoints (root and health) returning API description and status
2. run with : fastapi dev server_crud.py 
3. see the returned json (root() | "/") with : curl http://127.0.0.1:8000/ (output should be {"name":"Task API","version":"1.0","endpoints":["/tasks"]})
4. see the returned json (health() | "/health") : curl http://127.0.0.1:8000/health (output should be {"status":"ok"})





