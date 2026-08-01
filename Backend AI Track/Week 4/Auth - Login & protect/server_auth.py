from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse
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


@app.get("/public/info")
def public_info():
    return JSONResponse(
        status_code=200,
        content={"message": "Welcome stranger! This info is public."},
    )


@app.get("/protected/profile")
def protected_profile(authorization: Optional[str] = Header(default=None)):
    # Expect: "Authorization: Bearer <token>"
    if not authorization or not authorization.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={"error": "Access token required"},
        )

    token = authorization.removeprefix("Bearer ").strip()

    if not token:
        return JSONResponse(
            status_code=401,
            content={"error": "Access token required"},
        )

    # NOTE: token presence only — not verified yet, that's a later stage.
    return {"message": "Token received", "token_preview": token[:12] + "..."}


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


# to run: fastapi dev server_auth.py