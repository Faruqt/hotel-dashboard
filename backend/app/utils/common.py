# library imports
import logging
import math
import re
import os
from datetime import datetime
from weasyprint import HTML
from typing import Optional

# local imports
from app.config.settings import PDF_DIR_PATH, STATIC_DIR_PATH

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
    return re.sub(r"[^a-zA-Z0-9_-]", "", title.replace(" ", "_")).lower()


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


def calculate_pagination_metadata(
    current_page: int, page_size: int, total_items: int
) -> dict:
    """Calculate pagination metadata.

    Args:
        current_page (int): The current page number.
        page_size (int): The number of items per page.
        total_items (int): The total number of items.

    Returns:
        dict: A dictionary containing pagination metadata, including:
            - total_pages: Total number of pages
            - next_page: The next page number (None if on the last page)
            - prev_page: The previous page number (None if on the first page)
            - current_page: The current page number
            - page_size: The number of items per page
            - total_items: The total number of items
    """

    total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1

    return {
        "total_pages": total_pages,
        "next_page": current_page + 1 if current_page < total_pages else None,
        "prev_page": current_page - 1 if current_page > 1 else None,
        "current_page": current_page,
        "page_size": page_size,
        "total_items": total_items,
    }


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

        print("Creating PDF at path:", STATIC_DIR_PATH)

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
