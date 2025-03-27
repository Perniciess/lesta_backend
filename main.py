from fastapi import FastAPI
from app.controller import app_controller


app = FastAPI()
app.include_router(app_controller.router)