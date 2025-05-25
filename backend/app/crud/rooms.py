# library imports
import logging
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException

# local imports
from app.models.rooms import Room, RoomFacility
from app.schemas.rooms import RoomReadPaginated, RoomUpdate, RoomCreate

# create a logger instance
logger = logging.getLogger(__name__)


def get_rooms(
    db: Session,
    page: int,
    size: int,
) -> RoomReadPaginated:
    """
    Fetch a paginated list of rooms from the database.

    Args:
        db (Session): The database session.
        page (int): The page number to fetch.
        size (int): The number of rooms per page.

    Returns:
        RoomReadPaginated: A paginated response containing the rooms.

    Raises:
        Exception: If an error occurs while fetching rooms.
    """

    try:
        # Calculate the offset based on the page and size
        offset = (page - 1) * size

        # Fetch the rooms with pagination
        rooms = db.query(Room).offset(offset).limit(size + 1).all()

        has_next = len(rooms) > size
        if has_next:
            rooms = rooms[:-1]

        logger.info(f"Fetched {len(rooms)} rooms for page {page} with size {size}")

        return RoomReadPaginated(
            current_page=page,
            page_size=size,
            next_page=page + 1 if has_next else None,
            prev_page=page - 1 if page > 1 else None,
            data=rooms,
        )

    except Exception as e:
        # Log the error
        logger.error(f"An error occurred while fetching rooms: {e}", exc_info=True)
        raise


def get_room_by_id(db: Session, room_id: UUID) -> Room | None:
    """
    Fetch a room by its ID from the database.

    Args:
        db (Session): The database session.
        room_id (str): The ID of the room to fetch.

    Returns:
        Room | None: The Room object if found, otherwise None.

    Raises:
        Exception: If an error occurs while fetching the room.
    """

    try:
        # Fetch the room by ID from the database
        room = db.query(Room).filter(Room.id == room_id).first()

        logger.info(f"Successfully queried room with ID {room_id}")

        return room
    except Exception as e:
        # Log the error
        logger.error(
            f"An error occurred while fetching room with ID {room_id}: {e}",
            exc_info=True,
        )
        raise


def create_new_room(db: Session, room_data: RoomCreate) -> Room:
    """
    Create a new room in the database.

    Args:
        db (Session): The database session.
        room_data (RoomCreate): The data to create the room with.

    Returns:
        Room: The created Room object.

    Raises:
        Exception: If an error occurs while creating the room.
    """

    try:

        # Check if a room with the same title already exists
        existing_room = db.query(Room).filter(Room.title == room_data.title).first()
        if existing_room:
            logger.error(
                f"Room with title '{room_data.title}' already exists. Cannot create a new room."
            )
            raise HTTPException(
                status_code=400,
                detail=f"Room with title '{room_data.title}' already exists.",
            )

        # Create a new Room instance from the provided data
        # but exclude facilities for now
        new_room = Room(**room_data.dict(exclude={"facilities"}))

        # If facilities are provided, create them
        if room_data.facilities:
            create_room_facilities(db, new_room, room_data.facilities)

        # Add the new room to the session
        db.add(new_room)
        db.commit()

        # Refresh the room object to reflect the changes
        db.refresh(new_room)

        logger.info(f"Successfully created room with ID {new_room.id}")
        return new_room

    except Exception as e:
        db.rollback()  # Rollback the session in case of error
        logger.error(f"An error occurred while creating a new room: {e}", exc_info=True)
        raise


def update_room_and_facilities(db: Session, room_data: RoomUpdate, room: Room) -> Room:
    """
    Update a room in the database.

    Args:
        db (Session): The database session.
        room_data (RoomUpdate): The data to update the room with.
        room (Room): The Room object with updated data.

    Returns:
        Room: The updated Room object.

    Raises:
        Exception: If an error occurs while updating the room.
    """

    try:
        # Update room fields except facilities
        for key, value in room_data.dict(exclude={"facilities"}).items():
            if value not in [None, ""]:
                # Only update fields that are not None or empty
                new_value = value.strip() if isinstance(value, str) else value
                setattr(room, key, new_value)

        if room_data.facilities is not None:
            update_room_facilities(db, room, room_data.facilities)

        # Commit the changes to the database
        db.commit()

        # Refresh the room object to reflect the changes
        db.refresh(room)

        logger.info(f"Successfully updated room with ID {room.id}")
        return room

    except Exception as e:
        db.rollback()
        logger.error(
            f"An error occurred while trying to update room with ID {room.id}: {e}",
            exc_info=True,
        )
        raise


def create_room_facilities(db: Session, room: Room, facilities: list[str]) -> None:
    """
    Create facilities for a room in the database.

    Args:
        db (Session): The database session.
        room (Room): The Room object to associate facilities with.
        facilities (list[RoomFacilityCreate]): The list of facilities to create.

    Returns:
        None

    Raises:
        Exception: If an error occurs while creating the facilities.
    """

    new_facilities = []
    try:
        for facility in facilities:
            new_facility = RoomFacility(facility_name=facility.strip(), room=room)
            new_facilities.append(new_facility)

        # Bulk add the new facilities to the room
        db.add_all(new_facilities)

    except Exception as e:
        logger.error(
            f"An error occurred while trying to create facilities for room with ID {room.id}: {e}",
            exc_info=True,
        )
        raise


def update_room_facilities(db: Session, room: Room, facilities: list[str]) -> None:
    """
    Update the facilities of a room in the database.

    Args:
        db (Session): The database session.
        room (Room): The Room object to update.
        facilities (list[RoomFacilityUpdate]): The list of facilities to update.

    Returns:
        None

    Raises:
        Exception: If an error occurs while updating the facilities.
    """

    try:
        # Remove all existing facilities
        room.facilities.clear()

        # Add all facilities from the payload
        create_room_facilities(db, room, facilities)

        logger.info(f"Successfully replaced facilities for room with ID {room.id}")

    except Exception as e:
        logger.error(
            f"An error occurred while trying to update facilities for room with ID {room.id}: {e}",
            exc_info=True,
        )
        raise


def delete_room_entry(db: Session, room: Room) -> None:
    """
    Delete a room from the database.

    Args:
        db (Session): The database session.
        room (Room): The Room object to delete.

    Raises:
        Exception: If an error occurs while deleting the room.
    """

    try:
        room_id = room.id

        # Delete the room
        db.delete(room)
        db.commit()

        logger.info(f"Successfully deleted room with ID {room_id}")
    except Exception as e:
        db.rollback()  # Rollback the session in case of error
        logger.error(
            f"An error occurred while trying to delete room with ID {room_id}: {e}",
            exc_info=True,
        )
        raise
