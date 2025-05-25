# library imports
from fastapi import FastAPI

# local imports
from app.database.base import Base, engine
from app.api.router import include_api_routes
from app.setup.static_mount import mount_static_files
from app.setup.logging_config import setup_logging
from app import models
from app.database.init_db import populate_data
from app.config.settings import IMAGE_DIR


# Initialize logging configuration
setup_logging()

app = FastAPI()


@app.on_event("startup")
def on_startup():
    """
    Startup event handler to create the database tables.
    """
    # Create the database tables if they don't exist
    Base.metadata.create_all(bind=engine)
    # Preload data into the database
    populate_data()


# Include the API router for various endpoints
include_api_routes(app)

# Serve images from the static/images directory
mount_static_files(app, url_path="/images", sub_dir=IMAGE_DIR)
