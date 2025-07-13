from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.database import Base, engine
from app.api import projects, weights


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(
    title="Decision Helper API",
    description="A FastAPI application for multi-criteria decision analysis.",
    lifespan=lifespan
)

app.include_router(projects.router)
app.include_router(weights.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Decision Helper API"}
