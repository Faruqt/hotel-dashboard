# library imports
import pytest
from unittest import mock
from fastapi import HTTPException
from uuid import uuid4


# local imports
from app.crud.rooms import (
    get_rooms,
    get_room_by_id,
    create_new_room,
    update_room_and_facilities,
    delete_room_entry,
    partial_update_room,
    check_if_room_with_title_exists,
    create_room_facilities,
    update_room_facilities,
)


@pytest.fixture
def fake_room_schema():
    schema = mock.Mock()
    schema.dict.return_value = {
        "title": "Deluxe Suite",
        "description": "A beautiful room",
        "facilities": ["WiFi", "TV"],
    }
    schema.title = "Deluxe Suite"
    schema.facilities = ["WiFi", "TV"]
    return schema


def test_get_rooms_success(fake_db, fake_room):
    fake_query = mock.Mock()
    fake_query.offset.return_value.limit.return_value.all.return_value = [
        fake_room,
        fake_room,
        fake_room,
    ]
    fake_db.query.return_value = fake_query
    with mock.patch(
        "app.crud.rooms.BaseRoomRead", side_effect=lambda **kwargs: mock.Mock(**kwargs)
    ), mock.patch(
        "app.crud.rooms.RoomReadPaginated",
        side_effect=lambda **kwargs: mock.Mock(**kwargs),
    ):
        result = get_rooms(fake_db, page=1, size=2)
        assert result.current_page == 1
        assert result.page_size == 2
        assert isinstance(result.data, list)


def test_get_rooms_exception(fake_db):
    fake_db.query.side_effect = Exception("DB error")
    with pytest.raises(Exception):
        get_rooms(fake_db, page=1, size=2)


def test_get_room_by_id_success(fake_db, fake_room):
    fake_query = mock.Mock()
    fake_query.filter.return_value.first.return_value = fake_room
    fake_db.query.return_value = fake_query
    result = get_room_by_id(fake_db, fake_room.id)
    assert result == fake_room


def test_get_room_by_id_exception(fake_db):
    fake_db.query.side_effect = Exception("DB error")
    with pytest.raises(Exception):
        get_room_by_id(fake_db, uuid4())


def test_create_new_room_success(fake_db, fake_room_schema):
    room_id = uuid4()
    with mock.patch("app.crud.rooms.check_if_room_with_title_exists"), mock.patch(
        "app.crud.rooms.Room", return_value=mock.Mock(id=room_id)
    ), mock.patch("app.crud.rooms.create_room_facilities"):
        fake_db.add = mock.Mock()
        fake_db.commit = mock.Mock()
        fake_db.refresh = mock.Mock()
        result = create_new_room(fake_db, fake_room_schema)
        assert hasattr(result, "id")
        assert result.id == room_id


def test_create_new_room_http_exception(fake_db, fake_room_schema):
    with mock.patch(
        "app.crud.rooms.check_if_room_with_title_exists",
        side_effect=HTTPException(status_code=400, detail="exists"),
    ):
        fake_db.rollback = mock.Mock()
        with pytest.raises(HTTPException):
            create_new_room(fake_db, fake_room_schema)


def test_create_new_room_general_exception(fake_db, fake_room_schema):
    with mock.patch(
        "app.crud.rooms.check_if_room_with_title_exists", side_effect=Exception("fail")
    ):
        fake_db.rollback = mock.Mock()
        with pytest.raises(Exception):
            create_new_room(fake_db, fake_room_schema)


def test_update_room_and_facilities_success(fake_db, fake_room_schema, fake_room):
    fake_room_schema.dict.return_value = {
        "title": "Deluxe Suite",
        "description": "desc",
    }
    fake_room_schema.title = "Deluxe Suite"
    fake_room_schema.facilities = ["WiFi"]
    with mock.patch("app.crud.rooms.check_if_room_with_title_exists"), mock.patch(
        "app.crud.rooms.update_room_facilities"
    ):
        fake_db.commit = mock.Mock()
        fake_db.refresh = mock.Mock()
        result = update_room_and_facilities(fake_db, fake_room_schema, fake_room)
        assert result == fake_room


def test_update_room_and_facilities_http_exception(
    fake_db, fake_room_schema, fake_room
):
    with mock.patch(
        "app.crud.rooms.check_if_room_with_title_exists",
        side_effect=HTTPException(status_code=400, detail="exists"),
    ):
        fake_db.rollback = mock.Mock()
        with pytest.raises(HTTPException):
            update_room_and_facilities(fake_db, fake_room_schema, fake_room)


def test_update_room_and_facilities_general_exception(
    fake_db, fake_room_schema, fake_room
):
    with mock.patch(
        "app.crud.rooms.check_if_room_with_title_exists", side_effect=Exception("fail")
    ):
        fake_db.rollback = mock.Mock()
        with pytest.raises(Exception):
            update_room_and_facilities(fake_db, fake_room_schema, fake_room)


def test_partial_update_room_success(fake_db, fake_room_schema, fake_room):
    fake_room_schema.dict.return_value = {"title": "Deluxe Suite"}
    fake_db.commit = mock.Mock()
    fake_db.refresh = mock.Mock()
    result = partial_update_room(fake_db, fake_room_schema, fake_room)
    assert result == fake_room


def test_partial_update_room_exception(fake_db, fake_room_schema, fake_room):
    fake_db.commit.side_effect = Exception("fail")
    fake_db.rollback = mock.Mock()
    with pytest.raises(Exception):
        partial_update_room(fake_db, fake_room_schema, fake_room)


def test_check_if_room_with_title_exists(fake_db):
    fake_query = mock.Mock()
    fake_query.filter.return_value = fake_query
    fake_query.first.return_value = True
    fake_db.query.return_value = fake_query
    with pytest.raises(HTTPException):
        check_if_room_with_title_exists(fake_db, "Deluxe Suite")


def test_check_if_room_with_title_does_not_exist(fake_db):
    fake_query = mock.Mock()
    fake_query.filter.return_value = fake_query
    fake_query.first.return_value = None
    fake_db.query.return_value = fake_query
    check_if_room_with_title_exists(fake_db, "Deluxe Suite")


def test_check_if_room_with_title_exists_exception(fake_db):
    fake_db.query.side_effect = Exception("fail")
    with pytest.raises(Exception):
        check_if_room_with_title_exists(fake_db, "Deluxe Suite")


def test_create_room_facilities_success(fake_db, fake_room):
    with mock.patch("app.crud.rooms.RoomFacility"):
        fake_db.add_all = mock.Mock()
        create_room_facilities(fake_db, fake_room, ["WiFi", "TV"])
        fake_db.add_all.assert_called()


def test_create_room_facilities_exception(fake_db, fake_room):
    fake_db.add_all.side_effect = Exception("fail")
    with pytest.raises(Exception):
        create_room_facilities(fake_db, fake_room, ["WiFi"])


def test_update_room_facilities_success(fake_db, fake_room):
    fake_room.facilities = mock.Mock()
    fake_room.facilities.clear = mock.Mock()
    with mock.patch("app.crud.rooms.create_room_facilities"):
        update_room_facilities(fake_db, fake_room, ["WiFi"])
        fake_room.facilities.clear.assert_called_once()


def test_update_room_facilities_exception(fake_db, fake_room):
    fake_room.facilities = mock.Mock()
    fake_room.facilities.clear = mock.Mock(side_effect=Exception("fail"))
    with pytest.raises(Exception):
        update_room_facilities(fake_db, fake_room, ["WiFi"])


def test_delete_room_entry_success(fake_db, fake_room):
    fake_db.delete = mock.Mock()
    fake_db.commit = mock.Mock()
    delete_room_entry(fake_db, fake_room)
    fake_db.delete.assert_called_once_with(fake_room)
    fake_db.commit.assert_called_once()


def test_delete_room_entry_exception(fake_db, fake_room):
    fake_db.delete.side_effect = Exception("fail")
    fake_db.rollback = mock.Mock()
    with pytest.raises(Exception):
        delete_room_entry(fake_db, fake_room)
