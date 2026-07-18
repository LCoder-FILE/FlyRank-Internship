
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


# Stage 3 - Create with validation

1. run the server_crud.py with : fastapi dev server_crud.py 
2. use curl command to add the task (both valid and empty task)
3. validate the new task with : curl http://127.0.0.1:8000/tasks


```cmd
(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship>curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Buy milk\"}"
HTTP/1.1 201 Created
date: Sat, 18 Jul 2026 09:38:09 GMT
server: uvicorn
content-length: 40
content-type: application/json

{"id":4,"title":"Buy milk","done":false}

(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship>curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d "{\"title\": \"\"}"
HTTP/1.1 400 Bad Request
date: Sat, 18 Jul 2026 09:38:16 GMT
server: uvicorn
content-length: 38
content-type: application/json

{"message":"Task's title is required"}

(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship>curl http://127.0.0.1:8000/tasks
[{"id":1,"title":"cook","done":false},{"id":2,"title":"laundry","done":true},{"id":3,"title":"study","done":false},{"id":4,"title":"Buy milk","done":false}]
```


# Stage 4 - Full CRUD

1. run the server_crud.py with : fastapi dev server_crud.py 
2. use curl command to do CRUD operation specified

```cmd
(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship>curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Go Exercise\"}"
HTTP/1.1 201 Created
date: Sat, 18 Jul 2026 13:04:30 GMT
server: uvicorn
content-length: 43
content-type: application/json

{"id":4,"title":"Go Exercise","done":false}


(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship>curl http://127.0.0.1:8000/tasks
[{"id":1,"title":"cook","done":false},{"id":2,"title":"laundry","done":true},{"id":3,"title":"study","done":false},{"id":4,"title":"Go Exercise","done":false}]


(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship>curl -i -X PUT http://127.0.0.1:8000/tasks/4 -H "Content-Type: application/json" -d "{\"title\":\"Buy oat milk\"}"
HTTP/1.1 200 OK
date: Sat, 18 Jul 2026 13:20:42 GMT
server: uvicorn
content-length: 44
content-type: application/json

{"id":4,"title":"Buy oat milk","done":false}


(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship>curl http://127.0.0.1:8000/tasks
[{"id":1,"title":"cook","done":false},{"id":2,"title":"laundry","done":true},{"id":3,"title":"study","done":false},{"id":4,"title":"Buy oat milk","done":false}]


(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship>curl -i -X PUT http://127.0.0.1:8000/tasks/3 -H "Content-Type: application/json" -d "{\"done\":true}"
HTTP/1.1 200 OK
date: Sat, 18 Jul 2026 13:21:10 GMT
server: uvicorn
content-length: 36
content-type: application/json

{"id":3,"title":"study","done":true}

(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship>curl -i -X DELETE http://127.0.0.1:8000/tasks/4
HTTP/1.1 204 No Content
date: Sat, 18 Jul 2026 13:25:33 GMT
server: uvicorn
content-type: application/json


(fenv-flyrank) D:\6.5th Semester CIT\flyrank\FlyRank-Internship>curl http://127.0.0.1:8000/tasks
[{"id":1,"title":"cook","done":false},{"id":2,"title":"laundry","done":true},{"id":3,"title":"study","done":false}]

```

# Stage 5 - Swagger UI

1. run the server_crud.py with : fastapi dev server_crud.py 
2. access http://127.0.0.1:8000/docs 

result:
- show pic in ./screenshot/Stage 5 - Swagger UI/Create.png
- show pic in ./screenshot/Stage 5 - Swagger UI/Read.png
- show pic in ./screenshot/Stage 5 - Swagger UI/Update.png
- show pic in ./screenshot/Stage 5 - Swagger UI/Delete.png


# Stage 6 - Publish and docs

1. git clone https://github.com/LCoder-FILE/FlyRank-Internship
2. See the result in FlyRank-Internship/Backend AI Track/Week 2/Build your first CRUD API



