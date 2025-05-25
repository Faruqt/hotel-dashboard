# library imports
import logging
import os
from uuid import UUID, uuid4
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from fastapi import HTTPException, UploadFile, File
from sqlalchemy.orm import Session

# local imports
from app.crud.rooms import get_room_by_id
from app.models.rooms import Room
from app.utils.common import create_pdf_from_html
from app.config.settings import IMAGE_DIR_PATH, TEMPLATES_DIR_PATH


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


def upload_image_file(file: UploadFile = File(...)) -> str:
    """
    Upload an image file to the image directory.

    Args:
        file (UploadFile): The image file to upload.

    Returns:
        str: The name of the uploaded image file.

    Raises:
        HTTPException: If the file is not provided, does not have a filename,
                       or is not an image.
    """

    try:
        # Check if the file is provided
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")

        # Check if the file has a filename
        if not file.filename:
            raise HTTPException(status_code=400, detail="File must have a filename")

        # Check if the uploaded file is an image
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Ensure the image directory exists
        os.makedirs(IMAGE_DIR_PATH, exist_ok=True)

        # make file name unique by adding a uuid
        file_name = f"{uuid4().hex}_{file.filename}"

        # Save the uploaded file to the image directory
        file_path = os.path.join(IMAGE_DIR_PATH, file_name)

        with open(file_path, "wb") as f:
            f.write(file.file.read())

        logger.info(f"Image uploaded successfully: {file_name}")

        # Return the name of the uploaded image file
        return file_name

    except Exception as e:
        logger.error(
            f"An error occurred while uploading the image file: {e}", exc_info=True
        )
        raise e


def cleanup_image_file(file_name: str) -> None:
    """
    Remove an image file from the image directory.

    Args:
        file_name (str): The name of the image file to remove.

    Returns:
        None

    Raises:
        HTTPException: If an error occurs while removing the image file.
    """
    try:

        # Full path to the image file
        file_path = os.path.join(IMAGE_DIR_PATH, file_name)

        # Check if the file exists before attempting to remove it
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Image file removed successfully: {file_name}")
        else:
            logger.warning(f"Image file not found for removal: {file_name}")

    except Exception as e:
        logger.error(
            f"An error occurred while removing the image file: {e}", exc_info=True
        )
        raise e


def safe_cleanup_image(image_name):
    try:
        cleanup_image_file(image_name)
    except Exception as cleanup_err:
        logger.error(
            f"Failed to cleanup image file {image_name}: {cleanup_err}", exc_info=True
        )


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
