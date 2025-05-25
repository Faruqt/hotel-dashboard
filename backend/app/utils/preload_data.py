# library imports
import logging
import json
import os
from sqlalchemy.orm import Session
from datetime import datetime

# local imports
from app.models.rooms import Room, RoomFacility
from app.utils.common import convert_string_to_datetime

# create a logger instance
logger = logging.getLogger(__name__)

DUMMY_DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/dummy_rooms.json")


def preload_rooms_with_facilities(db: Session) -> None:
    """
    Preload rooms with facilities into the database.

    Args:
        db (Session): The database session.

    Returns:
        None

    Raises:
        Exception: If an error occurs while preloading rooms with facilities.
    """

    try:
        with open(DUMMY_DATA_PATH, "r") as file:
            parsed_data = json.load(file)

            if parsed_data:
                # Iterate through the parsed data and create Room and RoomFacility instances
                for room_data in parsed_data:
                    # Check if a room with this name already exists
                    room_title = room_data.get("title")
                    if not room_title:
                        logger.error("Room title is missing in the data.")
                        continue

                    existing_room = db.query(Room).filter_by(title=room_title).first()
                    if not existing_room:
                        # Create a Room instance
                        room = create_room_from_data(room_data)

                        # Add the room to the session
                        db.add(room)
                        db.flush()

                        # Add room facilities
                        for facility_name in room_data.get("facilities", []):
                            if facility_name:
                                # Create a RoomFacility instance
                                room_facility = create_room_facility(
                                    facility_name,
                                    room.id,
                                )

                                # Add the room facility to the session
                                db.add(room_facility)

            # Commit the changes to the database
            db.commit()
    except Exception as e:
        logger.error(
            f"An error occurred while preloading rooms with facilities: {e}",
            exc_info=True,
        )

        # Rollback the session in case of an error
        db.rollback()

        # re raise the exception to be handled by the caller
        raise


def create_room_from_data(room_data) -> Room:
    """
    Create a Room instance from the provided data.

    Args:
        room_data (dict): The room data.

    Returns:
        Room: The created Room instance.
    """
    created_at = room_data.get("created_at", None)
    updated_at = room_data.get("updated_at", None)

    return Room(
        title=room_data.get("title"),
        description=room_data.get("description", ""),
        image=room_data.get("image", ""),
        created_at=(
            convert_string_to_datetime(created_at) if created_at else datetime.now()
        ),
        updated_at=(convert_string_to_datetime(updated_at) if updated_at else None),
    )


def create_room_facility(facility_name, room_id) -> RoomFacility:
    """
    Create a RoomFacility instance.

    Args:
        facility_name (str): The name of the facility.
        room_id (UUID): The ID of the room.

    Returns:
        RoomFacility: The created RoomFacility instance.
    """
    # Use the current datetime for created_at and updated_at
    now = datetime.now()

    return RoomFacility(
        facility_name=facility_name,
        room_id=room_id,
        created_at=now,
        updated_at=now,
    )
