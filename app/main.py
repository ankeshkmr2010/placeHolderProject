from fastapi import FastAPI

from app.drivers.configs.config import Config
from app.repos.llm_wrapper.llm_openai_impl import OpenAiLlmWrapper
from app.routers import base_router
from app.drivers.db.migrations import run_migration
from app.routers.bonsen_demo_router import bonsen_router


def fastapi_app() -> FastAPI:
    #run migrations
    run_migration()
    Config.init_config()
    OpenAiLlmWrapper.set_client(Config.OPEN_AI_API_KEY)
    fapp = FastAPI(title="My FastAPI App",version="0.1.0")
    fapp.add_api_route("/", lambda: {"message": "Welcome to the Ankesh's app!"}, methods=["GET"])
    fapp.include_router(base_router.router, prefix="/tests")
    fapp.include_router(bonsen_router, prefix="/bonsen", tags=["bonsen"])
    return fapp


if __name__ == "__main__":
    app = fastapi_app()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)