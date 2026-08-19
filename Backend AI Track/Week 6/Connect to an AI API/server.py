from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from typing import Optional

from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Application setup

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "SUPABASE_URL and SUPABASE_KEY must be set in your .env file. "
        "Use the Project URL and the Publishable (anon) key from "
        "Project Settings -> API Keys — never the secret/service_role key."
    )

supabase: Client = create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)

app = FastAPI()


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    # Lets dependencies raise HTTPException(detail={"error": "..."}) and have
    # that dict returned as-is, instead of FastAPI's default {"detail": {...}} wrapping.
    if isinstance(exc.detail, dict):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


# Confirmation function

@app.on_event("startup")
async def verify_supabase_connection():
    try:
        supabase.auth.get_session()
        print("Server running and connected to Supabase")
    except Exception as e:
        print(f"Error : {e}")


# GET functions

@app.get("/")
def read_root():
    return {"message": "FastAPI + Supabase is running"}


@app.get("/health")
def health_check():
    """Simple health check that confirms the Supabase client is configured."""
    return {
        "status": "ok",
        "supabase_url": SUPABASE_URL,
        "supabase_client_initialized": supabase is not None,
    }


# POST functions

class AuthRequest(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None


@app.post("/auth/signup")
def signup(payload: AuthRequest):
    # Server never trusts the client — validate before touching Supabase
    if not payload.email or not payload.password:
        return JSONResponse(
            status_code=400,
            content={"error": "Bad Request: email and password are required"},
        )

    try:
        result = supabase.auth.sign_up(
            {"email": payload.email, "password": payload.password}
        )
    except Exception as e:
        # Supabase's own validation errors (duplicate email, weak password, etc.)
        # are client-input problems, so surface as 400 rather than 500.
        return JSONResponse(status_code=400, content={"error": str(e)})

    return JSONResponse(
        status_code=201,
        content={"user": result.user.model_dump(mode="json") if result.user else None},
    )


@app.post("/auth/login")
def login(payload: AuthRequest):
    if not payload.email or not payload.password:
        return JSONResponse(
            status_code=400,
            content={"error": "Bad Request: email and password are required"},
        )

    try:
        result = supabase.auth.sign_in_with_password(
            {"email": payload.email, "password": payload.password}
        )
    except Exception:
        # Supabase throws on invalid credentials — map to the exact body
        # shape required: {"error": "..."}
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid login credentials"},
        )

    return JSONResponse(
        status_code=200,
        content={
            "access_token": result.session.access_token,
            "refresh_token": result.session.refresh_token,
        },
    )


# Public routes (Stage 2)

@app.get("/public/info")
def public_info():
    return JSONResponse(
        status_code=200,
        content={"message": "Welcome stranger! This info is public."},
    )


# Reusable auth guard (Stage 4) + Swagger security scheme (Stage 5)
# HTTPBearer registers a "bearerAuth" scheme in the OpenAPI doc. Any route
# whose dependency chain includes it gets a lock icon in Swagger, and the
# "Authorize" button lets you paste a token once and reuse it across routes.
# auto_error=False so we keep full control of the 401 body shape instead of
# FastAPI's default {"detail": "Not authenticated"}.

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)):
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=401, detail={"error": "Access token required"})

    token = credentials.credentials.strip()

    if not token:
        raise HTTPException(status_code=401, detail={"error": "Access token required"})

    # Real network call to Supabase — this is what makes the check trustworthy.
    try:
        result = supabase.auth.get_user(token)
    except Exception:
        raise HTTPException(status_code=401, detail={"error": "Invalid or expired token"})

    if not result or not result.user:
        raise HTTPException(status_code=401, detail={"error": "Invalid or expired token"})

    # Attach both the verified user and the raw token — routes like logout
    # need the token itself, not just the user object.
    return {"user": result.user, "token": token}


# Protected routes (Stage 3 + 4)

@app.get("/protected/profile")
def protected_profile(current=Depends(get_current_user)):
    user = current["user"]
    return JSONResponse(
        status_code=200,
        content={
            "id": user.id,
            "email": user.email,
            "created_at": user.created_at.isoformat() if hasattr(user.created_at, "isoformat") else str(user.created_at),
        },
    )


@app.get("/protected/dashboard")
def protected_dashboard(current=Depends(get_current_user)):
    # No new auth code — same guard, reused.
    user = current["user"]
    return JSONResponse(
        status_code=200,
        content={"message": f"Welcome to your dashboard, {user.email}."},
    )


@app.post("/auth/logout")
def logout(current=Depends(get_current_user)):
    try:
        supabase.auth.sign_out()
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

    return Response(status_code=204)


# to run: fastapi dev server_auth.py