import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4

# local imports
from app.schemas.rooms import RoomRead, RoomReadPaginated
from app.config.settings import DEFAULT_PAGINATION_SIZE

API_URL = "api/v1/rooms"


def generate_room_payload(
    title: str,
    description: str,
    facilities: str,
):
    """Generate a mock room payload for testing."""
    return {
        "title": title,
        "description": description,
        "facilities": facilities,
    }


def test_list_rooms_success(client):
    """Test listing rooms with pagination."""
    response = client.get(API_URL)
    assert response.status_code == 200
    assert "current_page" in response.json()
    assert response.json()["current_page"] == 1
    assert "page_size" in response.json()
    assert response.json()["page_size"] == DEFAULT_PAGINATION_SIZE
    assert "next_page" in response.json()
    assert response.json()["next_page"] is None
    assert "prev_page" in response.json()
    assert response.json()["prev_page"] is None
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)


def test_list_rooms_error(client):
    """Test error handling when fetching rooms."""
    with patch(
        "app.api.v1.rooms.get_rooms",
        side_effect=MagicMock(side_effect=Exception("Unexpected error")),
    ):
        response = client.get(API_URL)
        assert response.status_code == 500
        assert "unexpected error" in response.json()["detail"].lower()


def test_get_room_success(client):
    """Test getting a room by ID."""
    # create a room to ensure it exists
    with patch("app.api.v1.rooms.upload_image_file", return_value="img.jpg"):
        response = client.post(
            API_URL,
            data=generate_room_payload(
                title="Some old test room",
                description="This is a test room.",
                facilities='["WiFi", "Parking"]',
            ),
            files={"image": ("test.jpg", b"fake image data", "image/jpeg")},
        )
    assert response.status_code == 200
    room_id = response.json()["id"]
    assert room_id is not None
    assert response.json()["title"] == "Some old test room"

    response = client.get(f"{API_URL}/{room_id}")
    assert response.status_code == 200
    assert response.json()["id"] == room_id


def test_get_room_not_found(client):
    """Test getting a room that does not exist."""
    room_id = str(uuid4())
    response = client.get(f"{API_URL}/{room_id}")
    assert response.status_code == 404


def test_create_room(client):
    """Test creating a room with valid data."""
    with patch("app.api.v1.rooms.upload_image_file", return_value="img.jpg"):
        response = client.post(
            API_URL,
            data=generate_room_payload(
                title="A Test Room",
                description="This is a test room.",
                facilities='["AirConditioning", "Laundry"]',
            ),
            files={"image": ("test.jpg", b"fake image data", "image/jpeg")},
        )
        assert response.status_code == 200
        assert response.json()["title"] == "A Test Room"
        assert response.json()["description"] == "This is a test room."
        assert response.json()["facilities_list"] == [
            "AirConditioning",
            "Laundry",
        ]


def test_create_room_error_cleanup(client):
    """Test error handling when creating a room."""
    with patch(
        "app.api.v1.rooms.upload_image_file",
        side_effect=Exception("Image upload failed"),
    ):
        response = client.post(
            API_URL,
            data=generate_room_payload(
                title="Some Test Room",
                description="This is a new test room.",
                facilities='["WiFi", "Parking"]',
            ),
            files={"image": ("testing_image.jpg", b"fake image data", "image/jpeg")},
        )
        assert response.status_code == 500


def test_create_room_json_error(client):
    """Test error handling when creating a room with invalid JSON."""
    response = client.post(
        API_URL,
        data=generate_room_payload(
            title="Invalid Room",
            description="This room has invalid facilities.",
            facilities="not a json string",
        ),
        files={"image": ("tester.jpg", b"fake image data", "image/jpeg")},
    )
    assert response.status_code == 500


@pytest.mark.parametrize(
    "title, description, facilities, status_code",
    [
        (None, "desc", '["WiFi"]', 422),
        ("Test Room", None, '["WiFi"]', 422),
        ("Test Room", "desc", None, 422),
    ],
)
def test_create_room_form_validation_error(
    client, title, description, facilities, status_code
):
    """Test form validation errors when creating a room."""
    data = {}
    if title is not None:
        data["title"] = title
    if description is not None:
        data["description"] = description
    if facilities is not None:
        data["facilities"] = facilities

    response = client.post(
        API_URL,
        data=data,
        files={"image": ("testing_image2.jpg", b"fake image data", "image/jpeg")},
    )
    assert response.status_code == status_code
    assert "field required" in response.json()["detail"][0]["msg"].lower()


@pytest.mark.parametrize(
    "title, description, facilities, status_code",
    [
        ("", "desc", '["WiFi"]', 400),
        ("Test Room", "", '["WiFi"]', 400),
        ("Test Room", "desc", "", 400),
    ],
)
def test_create_room_empty_validation_error(
    client, title, description, facilities, status_code
):
    """Test empty field validation errors when creating a room."""
    data = {
        "title": title,
        "description": description,
        "facilities": facilities,
    }

    response = client.post(
        API_URL,
        data=data,
        files={"image": ("test_imager.jpg", b"fake image data", "image/jpeg")},
    )
    assert response.status_code == status_code


def test_create_room_no_image(client):
    """Test creating a room without an image."""
    response = client.post(
        API_URL,
        data=generate_room_payload(
            title="No Image Room",
            description="This room has no image.",
            facilities='["WiFi", "Parking"]',
        ),
    )
    assert response.status_code == 422


def test_create_room_no_data(client):
    """Test creating a room with no data."""
    response = client.post(
        API_URL,
        data={},
        files={"image": ("new_image.jpg", b"fake image data", "image/jpeg")},
    )
    assert response.status_code == 422
    assert "field required" in response.json()["detail"][0]["msg"].lower()


def test_create_room_duplicate_title(client):
    """Test creating a room with a duplicate title."""
    with patch("app.api.v1.rooms.upload_image_file", return_value="img.jpg"):
        response = client.post(
            API_URL,
            data=generate_room_payload(
                title="Duplicate Room",
                description="This room has a duplicate title.",
                facilities='["WiFi", "Parking"]',
            ),
            files={"image": ("test.jpg", b"fake image data", "image/jpeg")},
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Duplicate Room"

    # create the same room again to trigger duplicate title error
    response = client.post(
        API_URL,
        data=generate_room_payload(
            title="Duplicate Room",
            description="This room has a duplicate title.",
            facilities='["WiFi", "Parking"]',
        ),
        files={"image": ("test.jpg", b"fake image data", "image/jpeg")},
    )
    assert response.status_code == 400


def test_create_room_raise_exception(client):
    """Test creating a room that raises an exception during image upload."""
    with patch(
        "app.api.v1.rooms.upload_image_file", side_effect=Exception("Upload failed")
    ):
        response = client.post(
            API_URL,
            data=generate_room_payload(
                title="Room with Exception",
                description="This room will raise an exception.",
                facilities='["WiFi", "Parking"]',
            ),
            files={"image": ("test.jpg", b"fake image data", "image/jpeg")},
        )
        assert response.status_code == 500
        assert "unexpected error" in response.json()["detail"].lower()


def test_update_room_not_found(client):
    """Test updating a room that does not exist."""
    room_id = str(uuid4())

    response = client.put(
        f"/api/v1/rooms/{room_id}",
        data=generate_room_payload(
            title="Updated Room",
            description="Updated desc",
            facilities='["WiFi"]',
        ),
    )
    assert response.status_code == 404


@pytest.mark.parametrize(
    "title, description, facilities, status_code",
    [
        (None, "desc", '["WiFi"]', 422),
        ("Test Room", None, '["WiFi"]', 422),
        ("Test Room", "desc", None, 422),
    ],
)
def test_update_room_form_validation_error(
    client, title, description, facilities, status_code
):
    """Test form validation errors when updating a room."""
    room_id = str(uuid4())
    data = {}
    if title is not None:
        data["title"] = title
    if description is not None:
        data["description"] = description
    if facilities is not None:
        data["facilities"] = facilities

    response = client.put(
        f"/api/v1/rooms/{room_id}",
        data=data,
        files={"image": ("test.jpg", b"fake image data", "image/jpeg")},
    )
    assert response.status_code == status_code
    assert "field required" in response.json()["detail"][0]["msg"].lower()


def test_update_room_empty_validation_error(client):
    """Test empty field validation errors when updating a room."""
    room_id = str(uuid4())
    response = client.put(
        f"/api/v1/rooms/{room_id}",
        data=generate_room_payload(
            title="",
            description="desc",
            facilities='["WiFi"]',
        ),
        files={"image": ("test.jpg", b"fake image data", "image/jpeg")},
    )
    assert response.status_code == 400


def test_update_room_success(client):
    """Test updating a room with valid data."""
    # create a room to ensure it exists

    with patch("app.api.v1.rooms.upload_image_file", return_value="img.jpg"):
        response = client.post(
            API_URL,
            data=generate_room_payload(
                title="Old Room",
                description="This is an old room.",
                facilities='["WiFi", "Parking"]',
            ),
            files={"image": ("test.jpg", b"fake image data", "image/jpeg")},
        )
        assert response.status_code == 200
        room_id = response.json()["id"]
        assert room_id is not None

    response = client.put(
        f"{API_URL}/{room_id}",
        data=generate_room_payload(
            title="Updated Room",
            description="This is an updated room.",
            facilities='["WiFi", "Gym"]',
        ),
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Room"
    assert response.json()["description"] == "This is an updated room."


def test_delete_room_not_found(client):
    """Test deleting a room that does not exist."""
    room_id = str(uuid4())
    response = client.delete(f"{API_URL}/{room_id}")
    assert response.status_code == 404


def test_delete_room_success(client):
    """Test deleting a room that exists."""
    # create a room to ensure it exists
    with patch("app.api.v1.rooms.upload_image_file", return_value="img.jpg"):
        response = client.post(
            API_URL,
            data=generate_room_payload(
                title="Room to Delete",
                description="This room will be deleted.",
                facilities='["WiFi", "Parking"]',
            ),
            files={"image": ("test.jpg", b"fake image data", "image/jpeg")},
        )
        assert response.status_code == 200
        room_id = response.json()["id"]
        assert room_id is not None

    response = client.delete(f"{API_URL}/{room_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Room deleted successfully"


def test_generate_room_pdf_success(client):
    """Test getting a room PDF."""
    # create a room to ensure it exists
    with patch("app.api.v1.rooms.upload_image_file", return_value="img.jpg"):
        response = client.post(
            API_URL,
            data=generate_room_payload(
                title="PDF Room",
                description="This room will be converted to PDF.",
                facilities='["WiFi", "Parking"]',
            ),
            files={"image": ("test.jpg", b"fake image data", "image/jpeg")},
        )
        assert response.status_code == 200
        room_id = response.json()["id"]
        assert room_id is not None

    with patch("app.api.v1.rooms.create_room_pdf", return_value="room.pdf"):
        # Now request the PDF
        response = client.post(f"{API_URL}/{room_id}/pdf")
        assert response.status_code == 200
        assert "room.pdf" in response.json()["pdf_path"]


def test_generate_room_pdf_not_found(client):
    """Test getting a PDF for a room that does not exist."""
    room_id = str(uuid4())
    response = client.post(f"{API_URL}/{room_id}/pdf")
    assert response.status_code == 404
    assert "Room not found" in response.json()["detail"]


def test_generate_room_pdf_error(client):
    """Test error handling when generating a room PDF."""

    with patch("app.api.v1.rooms.upload_image_file", return_value="img.jpg"):
        response = client.post(
            API_URL,
            data=generate_room_payload(
                title="Error PDF Room",
                description="This room will raise an error during PDF generation.",
                facilities='["WiFi", "Parking"]',
            ),
            files={"image": ("test.jpg", b"fake image data", "image/jpeg")},
        )
        assert response.status_code == 200
        room_id = response.json()["id"]
        assert room_id is not None
    with patch(
        "app.api.v1.rooms.create_room_pdf",
        side_effect=Exception("PDF generation failed"),
    ):
        response = client.post(f"{API_URL}/{room_id}/pdf")
        assert response.status_code == 500
        assert "unexpected error" in response.json()["detail"].lower()


def test_generate_room_pdf_invalid_id(client):
    """Test getting a PDF for a room with an invalid ID."""
    response = client.post(f"{API_URL}/invalid-id/pdf")
    assert response.status_code == 422
