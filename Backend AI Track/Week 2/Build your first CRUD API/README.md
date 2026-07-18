
# Stage 0 - Hello, server

1. pip install "fastapi[standard]""
2. run the server_crud.py with : fastapi dev server_crud.py -> **use this one to run** & make sure in ./"Backend AI Track"/"Week 2"/"Build your first CRUD API"/
3. see the page with : curl -i http://127.0.0.1:8000/docs


# Stage 1 - Root and health endpoints

1. run the server_crud.py with : fastapi dev server_crud.py 
2. see the returned json (root() | "/") with : curl http://127.0.0.1:8000/ (output should be {"name":"Task API","version":"1.0","endpoints":["/tasks"]})
3. see the returned json (health() | "/health") : curl http://127.0.0.1:8000/health (output should be {"status":"ok"})


# Stage 2 - Read endpoints with 404

1. run the server_crud.py with : fastapi dev server_crud.py 
2. see the returned json (tasks()) with : curl http://127.0.0.1:8000/tasks 
3. search certain task with the id with : curl http://127.0.0.1:8000/tasks/id -> example : curl http://127.0.0.1:8000/tasks/2 -> {"id":2,"title":"laundry","done":true}
4. if no task linked to given id -> curl http://127.0.0.1:8000/tasks/4 -> return {"detail":{"error":"Task 4 not found"} }

```cmd
(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship>curl http://127.0.0.1:8000/tasks  
[{"id":1,"title":"cook","done":false},{"id":2,"title":"laundry","done":true},{"id":3,"title":"study","done":false}]
(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship>curl http://127.0.0.1:8000/tasks/2
{"id":2,"title":"laundry","done":true}
(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship>curl http://127.0.0.1:8000/tasks/4
{"detail":{"error":"Task 4 not found"} } 
```



