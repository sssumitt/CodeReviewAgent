# app/main.py

from fastapi import FastAPI
# Import StaticFiles and FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from .database import init_db
from .routers import reports

app = FastAPI(title="Code Review Assistant - Gemini 2.5 Pro")

# --- New Static File Configuration ---
BASE_DIR = Path(__file__).resolve().parent.parent

# Mount the static directory to serve CSS, JS, etc.
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

# Include the API endpoints from the reports router
app.include_router(reports.router)


@app.on_event("startup")
async def on_startup():
    # Create database tables on startup
    init_db()

@app.get("/", response_class=FileResponse, include_in_schema=False)
async def dashboard():
    """Serves the main dashboard HTML page from the templates directory."""
    return FileResponse(BASE_DIR / "templates/index.html")