from fastapi import FastAPI
from app.routers import base_router
from app.drivers.db.migrations import run_migration
from app.routers.unbound_demo_router import ub_demo


def fastapi_app() -> FastAPI:
    #run migrations
    run_migration()
    fapp = FastAPI(title="My FastAPI App",version="0.1.0")
    fapp.include_router(base_router.router, prefix="/items")
    fapp.include_router(ub_demo, prefix="/unbound_demo")
    return fapp


if __name__ == "__main__":
    app = fastapi_app()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)