#!/usr/bin/env python3
"""Lightweight server for the Cognitive Observatory."""
from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()

@app.get("/dashboard")
def observatory():
    """Serve the Cognitive Observatory."""
    observatory_path = os.path.join(os.path.dirname(__file__), "templates", "cognitive_observatory.html")
    if os.path.exists(observatory_path):
        return FileResponse(observatory_path)
    return {"error": "Observatory not found"}

@app.get("/")
def root():
    """Redirect to observatory."""
    return {"message": "Living AI Observatory - visit /dashboard"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
