# library imports
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from unittest import mock


# local imports
from main import app
from app.database.base import Base
from app.database.session import get_db


# Create a test engine and session
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def fake_db():
    return mock.Mock()


@pytest.fixture
def fake_room():
    room = mock.Mock()
    room.title = "Deluxe Suite"
    room.description = "A beautiful room"
    room.image = "image.jpg"
    room.facilities = ["WiFi", "TV"]
    room.created_at_str = "2024-01-01"
    room.updated_at_str = "2024-01-02"

    return room


# Dependency override
def override_get_db():
    """
    Override the get_db dependency to use the testing session.
    """

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """
    Automatically create tables once before all tests run.
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    """
    Create a test client for the FastAPI app.
    This client can be used to make requests to the app during tests.
    """
    # Ensure the database is created before running tests
    return TestClient(app)
