from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from Backend.routers.chat import router

app = FastAPI()

app.include_router(router)
frontend_directory = Path(__file__).resolve().parent.parent / "Frontend"
app.mount("/", StaticFiles(directory=frontend_directory, html=True), name="frontend")
