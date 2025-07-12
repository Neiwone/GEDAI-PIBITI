from fastapi import FastAPI
from app.api import projects, weights

app = FastAPI(
    title="Decision Helper API",
    description="A FastAPI application for multi-criteria decision analysis."
)

# Include the routers for projects and weights
app.include_router(projects.router)
app.include_router(weights.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Decision Helper API"}