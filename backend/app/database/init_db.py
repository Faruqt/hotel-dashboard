# library imports
import logging

# local imports
from app.database.session import get_db
from app.utils.preload_data import preload_rooms_with_facilities

# create a logger instance
logger = logging.getLogger(__name__)


def populate_data():
    """
    Preload data into the database.
    """
    gen = get_db()
    db = next(gen)

    try:
        preload_rooms_with_facilities(db)
    except Exception as e:
        # handle any exceptions that occur during data preloading
        logger.error(f"An error occurred while preloading data: {e}", exc_info=True)
    finally:
        # clean up the database session
        next(gen, None)
