import pytest
from uuid import uuid4
from unittest import mock
from fastapi import HTTPException

# local imports
from app.utils.rooms import (
    get_room_or_error,
    create_room_pdf,
)


def test_get_room_or_error_success(fake_db, fake_room):
    with mock.patch("app.utils.rooms.get_room_by_id", return_value=fake_room):
        result = get_room_or_error(fake_db, uuid4(), "view")
        assert result == fake_room


def test_get_room_or_error_no_room_id(fake_db):
    with pytest.raises(HTTPException) as exc:
        get_room_or_error(fake_db, None, "view")
    assert exc.value.status_code == 400
    assert exc.value.detail == "Room ID is required"


def test_get_room_or_error_room_not_found(fake_db):
    with mock.patch("app.utils.rooms.get_room_by_id", return_value=None):
        with pytest.raises(HTTPException) as exc:
            get_room_or_error(fake_db, uuid4(), "view")
        assert exc.value.status_code == 404
        assert exc.value.detail == "Room not found"


def test_create_room_pdf_success(fake_room):
    fake_pdf_name = "room.pdf"
    with mock.patch(
        "app.utils.rooms.env.get_template"
    ) as mock_get_template, mock.patch(
        "app.utils.rooms.create_pdf_from_html", return_value=fake_pdf_name
    ):
        mock_template = mock.Mock()
        mock_template.render.return_value = "<html>...</html>"
        mock_get_template.return_value = mock_template
        result = create_room_pdf(fake_room)
        assert result == fake_pdf_name


def test_create_room_pdf_template_error(fake_room):
    with mock.patch(
        "app.utils.rooms.env.get_template", side_effect=Exception("template error")
    ):
        with pytest.raises(Exception):
            create_room_pdf(fake_room)
