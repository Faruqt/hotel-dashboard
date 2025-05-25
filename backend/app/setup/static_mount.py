# library imports
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# local imports
from app.config.settings import STATIC_DIR


def mount_static_files(app: FastAPI, url_path: str, sub_dir: str) -> None:
    """
    Mount static files to the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
        url_path (str): The URL path to serve the static files from.
        sub_dir (str): The directory containing the specific static files to be served.

    Returns:
        None
    """

    # Construct the full path to the static directory
    static_dir = os.path.join(STATIC_DIR, sub_dir)

    # Mount the static directory to serve static files
    app.mount(url_path, StaticFiles(directory=static_dir), name="static")
