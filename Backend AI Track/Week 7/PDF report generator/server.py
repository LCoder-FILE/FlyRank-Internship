import json

from fastapi import FastAPI
from pathlib import Path


# Application setup

app = FastAPI()


# GET Functions

@app.get("/health")
def get_health():
    return { "status": "ok" } 



# to run : fastapi dev server.py