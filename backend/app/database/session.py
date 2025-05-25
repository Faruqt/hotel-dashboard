# local imports
from .base import SessionLocal


def get_db():
    """
    Dependency that provides a database session.
    Yields a database session and closes it after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
