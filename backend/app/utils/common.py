# library imports
import logging
import math
from datetime import datetime

# create a logger instance
logger = logging.getLogger(__name__)


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
