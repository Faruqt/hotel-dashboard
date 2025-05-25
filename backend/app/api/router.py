# library imports
from fastapi import FastAPI

# local imports
from app.api.v1 import rooms
from app.api import health_check


def include_api_routes(app: FastAPI) -> None:
    """
    Include the API routes in the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    # Include the API router for various endpoints
    app.include_router(health_check.router, prefix="", tags=["Health Check"])
    app.include_router(rooms.router, prefix="/api/v1/rooms", tags=["Rooms"])
