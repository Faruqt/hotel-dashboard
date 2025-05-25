# library imports
import logging
from fastapi import APIRouter

# create a logger instance
logger = logging.getLogger(__name__)

# create a router instance
router = APIRouter()


@router.get("/")
def health_check() -> dict:
    """
    Health check endpoint to verify the API is running.

    Returns:
        dict: A dictionary containing the status of the API.
    """
    # Log the health check request
    logger.info("Health check endpoint called")
    return {"status": "ok"}
