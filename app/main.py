from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers import base_router
from app.drivers.db.migrations import run_migration
from app.routers import instead_demo_router

def fastapi_app() -> FastAPI:
    #run migrations
    run_migration()
    fapp = FastAPI(title="My FastAPI App",version="0.1.0")
    fapp.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Or ["http://localhost:5173"] for stricter setup
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    fapp.include_router(base_router.router, prefix="/items")
    fapp.include_router(instead_demo_router.ir, prefix="/instead")
    return fapp

app = fastapi_app()

if __name__ == "__main__":
    app = fastapi_app()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)