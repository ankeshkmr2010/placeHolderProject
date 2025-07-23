from fastapi import FastAPI
from app.routers import base_router

app = FastAPI(
    title="My FastAPI App",
    version="0.1.0",
)

app.include_router(base_router.router, prefix="/items")

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}
