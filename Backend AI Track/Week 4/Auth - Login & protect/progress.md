
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

{"user":{"id":"805be842-3cc7-4675-8340-8a68a1a5a086","app_metadata":{"provider":"email","providers":["email"]},"user_metadata":{"email":"test@example.com","email_verified":true,"phone_verified":false,"sub":"805be842-3cc7-4675-8340-8a68a1a5a086"},"aud":"authenticated","confirmation_sent_at":null,"recovery_sent_at":null,"email_change_sent_at":null,"new_email":null,"new_phone":null,"invited_at":null,"action_link":null,"email":"test@example.com","phone":"","created_at":"2026-08-01T13:50:51.168658Z","confirmed_at":null,"email_confirmed_at":"2026-08-01T13:50:51.180687Z","phone_confirmed_at":null,"last_sign_in_at":"2026-08-01T13:50:51.185183Z","role":"authenticated","updated_at":"2026-08-01T13:50:51.191457Z","identities":[{"id":"805be842-3cc7-4675-8340-8a68a1a5a086","identity_id":"60e46b81-2e3b-4890-b06f-9c7bfe2b9980","user_id":"805be842-3cc7-4675-8340-8a68a1a5a086","identity_data":{"email":"test@example.com","email_verified":true,"phone_verified":false,"sub":"805be842-3cc7-4675-8340-8a68a1a5a086"},"provider":"email","created_at":"2026-08-01T13:50:51.177343Z","last_sign_in_at":"2026-08-01T13:50:51.177304Z","updated_at":"2026-08-01T13:50:51.177343Z"}],"is_anonymous":false,"is_sso_user":false,"factors":null,"deleted_at":null,"banned_until":null}}


curl -i -X POST http://127.0.0.1:8000/auth/login -H "Content-Type: application/json" -d "{\"email\":\"test@example.com\",\"password\":\"password123\"}"

HTTP/1.1 200 OK
date: Sat, 01 Aug 2026 13:51:33 GMT
server: uvicorn
content-length: 970
content-type: application/json

{"access_token":"eyJhbGciOiJFUzI1NiIsImtpZCI6IjcxOWM0NDk1LWE3YWItNDI3Yy1iZGI0LWViZGZlOWNlODY2ZSIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2pzeWZodWF1b2N0cnRrYWl1a3NmLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI4MDViZTg0Mi0zY2M3LTQ2NzUtODM0MC04YTY4YTFhNWEwODYiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzg1NTk1ODk0LCJpYXQiOjE3ODU1OTIyOTQsImVtYWlsIjoidGVzdEBleGFtcGxlLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWwiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwic3ViIjoiODA1YmU4NDItM2NjNy00Njc1LTgzNDAtOGE2OGExYTVhMDg2In0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE3ODU1OTIyOTR9XSwic2Vzc2lvbl9pZCI6IjEyOWNjNjdmLTNlNmItNDUxZS1iNWM0LWI2NzE0YzQwZTBlMyIsImlzX2Fub255bW91cyI6ZmFsc2V9.LNMyLVR0tuMAPCQV_q64RaH0ivMW72ku44bjcUapGl-E15zqfQapZzTha60VRgo8dWNWmNdg_rrvgR4viCX8Ww","refresh_token":"s542trab3yqy"}


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