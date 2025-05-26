# library imports
from fastapi import FastAPI
from contextlib import asynccontextmanager

# local imports
from app.database.base import Base, engine
from app.api.router import include_api_routes
from app.setup.static_mount import mount_static_files
from app.setup.logging_config import setup_logging
from app import models
from app.database.init_db import populate_data
from app.config.settings import IMAGE_DIR, PDF_DIR


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup event handler to create the database tables.
    """
    # Initialize logging configuration
    setup_logging()

    # Create the database tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Preload data into the database
    populate_data()

    yield


# create the FastAPI application instance
app = FastAPI(lifespan=lifespan)

# Include the API router for various endpoints
include_api_routes(app)

# Serve images from the static/images directory
mount_static_files(app, url_path=f"/{IMAGE_DIR}", sub_dir=IMAGE_DIR)
# Serve pdf from the static/pdf directory
mount_static_files(app, url_path=f"/{PDF_DIR}", sub_dir=PDF_DIR)
