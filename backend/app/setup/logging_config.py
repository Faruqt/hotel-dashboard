import logging


def setup_logging():
    """
    Set up logging configuration for the application.
    This function configures the logging level and format for the application.
    """
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
