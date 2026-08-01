
# Stage 0

## Checkpoints

```cmd
fastapi dev server_auth.py

 ⚡️ Starting FastAPI in development mode
 
 🐍 Using import string: server_auth:app
 
 🌐 Server started at http://127.0.0.1:8000
    Documentation at http://127.0.0.1:8000/docs
 
  Logs:
 
 ▕  Will watch for changes in these directories: ['D:\\6.5th Semester 
    CIT\\flyrank\\FlyRank-Internship\\Backend AI Track\\Week 4\\Auth - Login & 
    protect']
 ▕  Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
 ▕  Started reloader process [1792] using WatchFiles
 ▕  Started server process [29200]
 ▕  Waiting for application startup.
Server running and connected to Supabase
 ▕  Application startup complete.
```

## Commit

```cmd
Stage 0: setup server and supabase client
```

---

# Stage 1

## Checkpoints

```cmd
curl -i -X POST http://127.0.0.1:8000/auth/signup -H "Content-Type: application/json" -d "{\"email\":\"test@example.com\",\"password\":\"password123\"}"

HTTP/1.1 201 Created
date: Sat, 01 Aug 2026 13:50:50 GMT
server: uvicorn
content-length: 1257
content-type: application/json

{"user":{"id":"my_id","app_metadata":{"provider":"email","providers":["email"]},"user_metadata":{"email":"test@example.com","email_verified":true,"phone_verified":false,"sub":"my_id"},"aud":"authenticated","confirmation_sent_at":null,"recovery_sent_at":null,"email_change_sent_at":null,"new_email":null,"new_phone":null,"invited_at":null,"action_link":null,"email":"test@example.com","phone":"","created_at":"2026-08-01T13:50:51.168658Z","confirmed_at":null,"email_confirmed_at":"2026-08-01T13:50:51.180687Z","phone_confirmed_at":null,"last_sign_in_at":"2026-08-01T13:50:51.185183Z","role":"authenticated","updated_at":"2026-08-01T13:50:51.191457Z","identities":[{"id":"my_id","identity_id":"my_identity_id","user_id":"my_id","identity_data":{"email":"test@example.com","email_verified":true,"phone_verified":false,"sub":"my_id"},"provider":"email","created_at":"2026-08-01T13:50:51.177343Z","last_sign_in_at":"2026-08-01T13:50:51.177304Z","updated_at":"2026-08-01T13:50:51.177343Z"}],"is_anonymous":false,"is_sso_user":false,"factors":null,"deleted_at":null,"banned_until":null}}


curl -i -X POST http://127.0.0.1:8000/auth/login -H "Content-Type: application/json" -d "{\"email\":\"test@example.com\",\"password\":\"password123\"}"

HTTP/1.1 200 OK
date: Sat, 01 Aug 2026 13:51:33 GMT
server: uvicorn
content-length: 970
content-type: application/json

{"access_token":"my_access_token","refresh_token":"my_refresh_token"}


curl -i -X POST http://127.0.0.1:8000/auth/signup -H "Content-Type: application/json" -d "{\"email\":\"test2@example.com\"}"

HTTP/1.1 400 Bad Request
date: Sat, 01 Aug 2026 13:52:23 GMT
server: uvicorn
content-length: 56
content-type: application/json

{"error":"Bad Request: email and password are required"}

```

## Commit

```cmd
Stage 1: signup and login routes working
```

---

# Stage 2

## Checkpoints

```cmd
curl -i http://127.0.0.1:8000/public/info

HTTP/1.1 200 OK
date: Sat, 01 Aug 2026 13:57:24 GMT
server: uvicorn
content-length: 52
content-type: application/json

{"message":"Welcome stranger! This info is public."}


curl -i http://127.0.0.1:8000/protected/profile

HTTP/1.1 401 Unauthorized
date: Sat, 01 Aug 2026 13:57:36 GMT
server: uvicorn
content-length: 33
content-type: application/json

{"error":"Access token required"}
```

## Commit

```cmd
Stage 2: public route and unverified protected route
```

---

# Stage 3

## Checkpoints

```cmd
curl -i -X POST http://127.0.0.1:8000/auth/login -H "Content-Type: application/json" -d "{\"email\":\"test@example.com\",\"password\":\"password123\"}"

HTTP/1.1 200 OK
date: Sat, 01 Aug 2026 14:01:39 GMT
server: uvicorn
content-length: 970
content-type: application/json

{"access_token":"my_access_token","refresh_token":"my_refresh_token"}


curl -i http://127.0.0.1:8000/protected/profile -H "Authorization: Bearer my_access_token"

HTTP/1.1 200 OK
date: Sat, 01 Aug 2026 14:02:33 GMT
server: uvicorn
content-length: 120
content-type: application/json

{"id":"my_id","email":"test@example.com","created_at":"2026-08-01T13:50:51.168658+00:00"}

```

## Commit

```cmd
Stage 3: profile route token verification
```

---

# Stage 4

## Checkpoints

```cmd
curl -i -X POST http://127.0.0.1:8000/auth/login -H "Content-Type: application/json" -d "{\"email\":\"test@example.com\",\"password\":\"password123\"}"

HTTP/1.1 200 OK
date: Sat, 01 Aug 2026 14:24:18 GMT
server: uvicorn
content-length: 970
content-type: application/json

{"access_token":"my_access_token","refresh_token":"my_refresh_token"}


curl -i http://127.0.0.1:8000/protected/dashboard -H "Authorization: Bearer my_access_token"

HTTP/1.1 200 OK
date: Sat, 01 Aug 2026 14:26:58 GMT
server: uvicorn
content-length: 58
content-type: application/json

{"message":"Welcome to your dashboard, test@example.com."}


curl -i http://127.0.0.1:8000/protected/dashboard -H "Authorization: Bearer garbage"

HTTP/1.1 401 Unauthorized
date: Sat, 01 Aug 2026 14:27:22 GMT
server: uvicorn
content-length: 36
content-type: application/json

{"error":"Invalid or expired token"}


curl -i -X POST http://127.0.0.1:8000/auth/logout -H "Authorization: Bearer my_access_token"

HTTP/1.1 204 No Content
date: Sat, 01 Aug 2026 14:28:18 GMT
server: uvicorn
```

## Commit

```cmd
Stage 4: auth middleware and logout endpoint
```

---

# Stage 5

## Checkpoints

```cmd
curl -i -X POST http://127.0.0.1:8000/auth/login -H "Content-Type: application/json" -d "{\"email\":\"test@example.com\",\"password\":\"password123\"}"

HTTP/1.1 200 OK
date: Sat, 01 Aug 2026 14:24:18 GMT
server: uvicorn
content-length: 970
content-type: application/json

{"access_token":"my_access_token","refresh_token":"my_refresh_token"}
```

![Successful auth](./screenshot/swagger_ui.png)

## Commit

```cmd
Stage 5: Swagger UI documentation with bearer auth
```

---

# Stage 6

## Commit

```cmd
Stage 6: publish to GitHub and write README — then push everything.
```