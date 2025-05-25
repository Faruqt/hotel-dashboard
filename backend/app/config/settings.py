import os

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sqlite.db")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
IMAGE_DIR = "images"
DATE_OUTPUT_FORMAT = "%d/%m/%Y"
MAX_PAGINATION_LIMIT = 100
DEFAULT_PAGINATION_SIZE = 20
