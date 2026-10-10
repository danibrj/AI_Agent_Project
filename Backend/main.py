from fastapi import FastAPI

from Backend.routers.chat import router

app = FastAPI()

app.include_router(router)
