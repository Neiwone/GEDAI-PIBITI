from fastapi import FastAPI
from app.api import weights

app = FastAPI(title="Decision Helper API")

app.include_router(weights.router, prefix="/api")
