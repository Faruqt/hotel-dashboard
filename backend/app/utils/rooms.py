# library imports
import logging
import os
from uuid import UUID
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from fastapi import HTTPException
from sqlalchemy.orm import Session

# local imports
from app.crud.rooms import get_room_by_id
from app.models.rooms import Room
from app.utils.common import create_pdf_from_html
from app.config.settings import TEMPLATES_DIR_PATH


# create a logger instance
logger = logging.getLogger(__name__)

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR_PATH))


def get_room_or_error(db: Session, room_id: UUID, action: str) -> Room:
    """
    Fetch a room by ID or raise an HTTPException if not found.

    Args:
        db (Session): The database session.
        room_id (str): The ID of the room to fetch.
        action (str): The action being performed, used for logging.

    Returns:
        Room: The Room object if found.

    Raises:
        HTTPException: If the room is not found or if the room ID is not provided.
    """

    try:
        # Check if room_id is provided
        if not room_id:
            logger.warning(f"Room ID is required for {action} operation")
            raise HTTPException(status_code=400, detail="Room ID is required")

        # Fetch the room to check if it exists
        room = get_room_by_id(db=db, room_id=room_id)

        # If the room is not found, raise a 404 error
        if not room:
            logger.warning(f"Room with ID {room_id} not found for {action} operation")
            raise HTTPException(status_code=404, detail="Room not found")

        # Log the successful retrieval of the room
        logger.info(
            f"Successfully retrieved room with ID {room_id} for {action} operation"
        )

        return room

    except Exception as e:
        logger.error(
            f"An error occurred while fetching room with ID {room_id}: {e}",
            exc_info=True,
        )
        raise e


def create_room_pdf(room: Room) -> str:
    """
    Create a PDF for a room using its details.

    Args:
        room (Room): The Room object containing details to be included in the PDF.

    Returns:
        pdf_name (str): The name of the created PDF file.

    Raises:
        HTTPException: If an error occurs while creating the PDF.
    """
    try:

        # get current year
        current_year = datetime.now().year

        # Ensure the templates directory exists
        template = env.get_template("room_template.html")

        context = {
            "title": room.title,
            "description": room.description,
            "image": room.image,
            "facilities": room.facilities_list,
            "created_at": room.created_at_str,
            "year": current_year,
        }

        html_out = template.render(**context)

        # Generate the PDF file
        pdf_name = create_pdf_from_html(
            pdf_name=room.title,
            html_content=html_out,
            caller="Room PDF Creation",
        )

        logger.info(f"PDF created successfully: {pdf_name}")

        return pdf_name

    except Exception as e:
        logger.error(
            f"An error occurred while creating PDF for room {room.title}: {e}",
            exc_info=True,
        )
        raise e
