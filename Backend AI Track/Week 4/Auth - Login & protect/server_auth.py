from fastapi import FastAPI, HTTPException
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





# to run : fastapi dev server_auth.py (use this one & make sure in ./Backend AI Track/Week 4/Auth - Login & protect/)

