import logging
from typing import Dict

from fastapi import FastAPI

from app.drivers.configs.config import Config
from app.drivers.db.migrations import run_migration
from app.repos.llm_wrapper.llm_openai_impl import OpenAiLlmWrapper
from app.routers import base_router
from app.routers.bonsen_demo_router import bonsen_router

# Configure logging for the application
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # Define the log message format
)
logger = logging.getLogger(__name__)  # Create a logger instance for the current module


def fastapi_app() -> FastAPI:
    """
    Initializes and configures the FastAPI application.

    This function performs the following tasks:
    - Runs database migrations.
    - Initializes application configuration.
    - Sets up the OpenAI LLM client using the API key from the configuration.
    - Creates a FastAPI application instance.
    - Adds a root route for a "Hello, World!" message.
    - Includes routers for additional endpoints.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    # Initialize application configuration
    Config.init_config()

    # Run database migrations
    run_migration()


    # Set up the OpenAI LLM client
    OpenAiLlmWrapper.set_client(Config.OPEN_AI_API_KEY)

    # Create the FastAPI application instance
    fapp = FastAPI(title="My FastAPI App", version="0.1.0")

    # Add a root route for a "Hello, World!" message
    fapp.add_api_route("/", hello_world, methods=["GET"])

    # Include routers for additional endpoints
    fapp.include_router(base_router.router, prefix="/tests")
    fapp.include_router(bonsen_router, prefix="/bonsen", tags=["bonsen"])

    return fapp


def hello_world() -> Dict[str, str]:
    """
    A simple endpoint that returns a "Hello, World!" message.

    Returns:
        Dict[str, str]: A dictionary containing the message.
    """
    return {"message": "Hello, World!"}

app = fastapi_app()  # Create the FastAPI application instance

# Create the FastAPI application instance
if __name__ == "__main__":
    """
    Entry point for running the FastAPI application.

    This block starts the FastAPI application using Uvicorn as the ASGI server.
    """
    logger.info("Starting FastAPI application...")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)


