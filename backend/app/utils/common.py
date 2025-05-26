# library imports
import logging
import re
import os
from uuid import UUID, uuid4
from datetime import datetime
from weasyprint import HTML
from fastapi import HTTPException, UploadFile, File


# local imports
from app.config.settings import PDF_DIR_PATH, STATIC_DIR_PATH, IMAGE_DIR_PATH


# create a logger instance
logger = logging.getLogger(__name__)


def sanitize_filename(title: str) -> str:
    """
    Sanitize a filename by replacing spaces with underscores and removing non-alphanumeric characters.

    Args:
        title (str): The title to sanitize.

    Returns:
        str: The sanitized filename.
    """
    # Replace spaces with underscores and remove non-alphanumeric characters
    return re.sub(r"[^a-zA-Z0-9_-]", "", title.strip().replace(" ", "_")).lower()


def convert_string_to_datetime(date_string: str) -> datetime:
    """
    Convert a string to a datetime object.

    Args:
        date_string (str): The date string to convert.

    Returns:
        datetime: The converted datetime object.

    Raises:
        ValueError: If the date string is not in the expected format.
        Exception: If an unexpected error occurs during conversion.
    """
    try:
        return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        try:
            # Fallback if microseconds are missing
            return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            logger.error(f"Error converting string to datetime: {e}", exc_info=True)
            raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        raise


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


def create_pdf_from_html(
    pdf_name: str,
    html_content: str,
    caller: str,
) -> str:
    """
    Create a PDF using a rendered HTML template.

    Args:
        pdf_name (str): The name for the PDF file to be created.
        html_content (str): The HTML content to render in the PDF.
        caller (str): The caller of the function, used for logging.

    Returns:
        sanitized_name (str): The name of the created PDF file.

    Raises:
        HTTPException: If an error occurs while creating the PDF.
    """
    try:
        # Ensure the PDF directory exists
        os.makedirs(PDF_DIR_PATH, exist_ok=True)

        sanitized_name = sanitize_filename(pdf_name) + ".pdf"
        logger.info(
            f"PDF with name: {pdf_name} created successfully created for {caller}"
        )

        pdf_path = os.path.join(PDF_DIR_PATH, sanitized_name)

        HTML(string=html_content, base_url=STATIC_DIR_PATH).write_pdf(
            pdf_path,
        )

        return sanitized_name

    except Exception as e:
        logger.error(
            f"An error occurred while creating PD from html content for {caller}: {e}",
            exc_info=True,
        )
        raise e
