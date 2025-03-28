from fastapi import FastAPI
from app import controller


app = FastAPI()
app.include_router(controller.router)