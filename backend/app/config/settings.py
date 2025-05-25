import os

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sqlite.db")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
STATIC_DIR_PATH = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR_PATH = os.path.join(BASE_DIR, "templates")
IMAGE_DIR = "images"
IMAGE_DIR_PATH = os.path.join(STATIC_DIR_PATH, IMAGE_DIR)
PDF_DIR = "pdfs"
PDF_DIR_PATH = os.path.join(STATIC_DIR_PATH, PDF_DIR)
DATE_OUTPUT_FORMAT = "%d/%m/%Y"
MAX_PAGINATION_LIMIT = 100
DEFAULT_PAGINATION_SIZE = 20
APP_URL = os.getenv("APP_URL", "http://127.0.1:8000")
