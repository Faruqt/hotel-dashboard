# library imports
import logging
import json
from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session

# local imports
from app.database.session import get_db
from app.schemas.rooms import (
    RoomReadPaginated,
    RoomRead,
    RoomCompleteUpdate,
    RoomPartialUpdate,
    RoomCreate,
)
from app.crud.rooms import (
    get_rooms,
    create_new_room,
    update_room_and_facilities,
    delete_room_entry,
    partial_update_room,
)
from app.utils.rooms import (
    get_room_or_error,
    upload_image_file,
    safe_cleanup_image,
    create_room_pdf,
)
from app.config.settings import MAX_PAGINATION_LIMIT, DEFAULT_PAGINATION_SIZE

# create a logger instance
logger = logging.getLogger(__name__)

# create a router instance
router = APIRouter()


@router.get("/", response_model=RoomReadPaginated)
def list_rooms(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(DEFAULT_PAGINATION_SIZE, ge=1, le=MAX_PAGINATION_LIMIT),
) -> RoomReadPaginated:
    """
    List all rooms.

    Args:
        db (Session): The database session.

    Returns:
        RoomReadPaginated: A paginated response containing the rooms and pagination metadata.

    Raises:
        HTTPException: If an unexpected error occurs while fetching rooms.
    """
    try:
        # Fetch rooms from the database
        rooms_response = get_rooms(db, page, size)

        return rooms_response

    except Exception as e:
        logger.error(f"An error occurred while fetching rooms: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred while fetching rooms"
        )


@router.get("/{room_id}", response_model=RoomRead)
def get_room(room_id: UUID, db: Session = Depends(get_db)) -> RoomRead:
    """
    Get a specific room by ID.

    Args:
        room_id (UUID): The ID of the room to fetch.
        db (Session): The database session.

    Returns:
        RoomRead: The RoomRead object for the specified room.

    Raises:
        HTTPException: If the room is not found or if an unexpected error occurs.
    """
    try:
        room = get_room_or_error(db=db, room_id=room_id, action="fetching")

        return room
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(
            f"An error occurred while fetching the room with ID {room_id}: {e}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while fetching the room",
        )


@router.post("/", response_model=RoomRead)
def create_room(
    title: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...),
    facilities: str = Form(...),
    db: Session = Depends(get_db),
) -> RoomRead:
    """
    Create a new room.

    Args:
        title (str): The title of the room.
        description (str): The description of the room.
        image (UploadFile): The image file for the room.
        facilities (str): A JSON string representing the facilities associated with the room.
        db (Session): The database session.

    Returns:
        RoomRead: The created RoomRead object.

    Raises:
        HTTPException: If an unexpected error occurs while creating the room.
    """
    try:

        # Upload the image file and get the image name
        image_name = upload_image_file(file=image)

        # Prepare the room data
        room_data = RoomCreate(
            title=title.strip(),
            description=description.strip(),
            image=image_name,
            facilities=json.loads(facilities) if facilities else [],
        )
        # Create a new room and its facilities
        room = create_new_room(db=db, room_data=room_data)

        return room

    except HTTPException as e:
        logger.error(
            f"An error occurred while creating the room: {e.detail}", exc_info=True
        )
        if "image_name" in locals():
            safe_cleanup_image(image_name)
        raise e
    except Exception as e:
        logger.error(f"An error occurred while creating the room: {e}", exc_info=True)
        if "image_name" in locals():
            safe_cleanup_image(image_name)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while creating the room",
        )


@router.put("/{room_id}", response_model=RoomRead)
def update_room(
    room_id: UUID,
    title: str = Form(...),
    description: str = Form(...),
    image: Optional[UploadFile] = File(None),
    facilities: str = Form(...),
    db: Session = Depends(get_db),
) -> RoomRead:
    """
    Update a specific room by ID.

    Args:
        room_id (UUID): The ID of the room to update.
        title (str): The new title of the room.
        description (str): The new description of the room.
        image (Optional[UploadFile]): The new image file for the room (optional).
        facilities (str): A JSON string representing the new facilities associated with the room.
        db (Session): The database session.

    Returns:
        RoomRead: The updated RoomRead object.

    Raises:
        HTTPException: If the room is not found or if an unexpected error occurs.
    """
    try:
        existing_room = get_room_or_error(db=db, room_id=room_id, action="update")

        # Only upload a new image if one is provided
        if image is not None and image.filename:
            image_name = upload_image_file(file=image)
        else:
            image_name = existing_room.image

        room_data = RoomCompleteUpdate(
            title=title.strip(),
            description=description.strip(),
            image=image_name,
            facilities=json.loads(facilities) if facilities else [],
        )

        room = update_room_and_facilities(
            db=db,
            room_data=room_data,
            room=existing_room,
        )

        return room

    except HTTPException as e:
        if "image_name" in locals():
            safe_cleanup_image(image_name)
        raise e
    except Exception as e:
        logger.error(
            f"An error occurred while updating the room with ID {room_id}: {e}",
            exc_info=True,
        )
        if "image_name" in locals():
            safe_cleanup_image(image_name)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while updating the room",
        )


@router.post("/{room_id}/pdf", response_model=RoomRead)
def create_pdf(room_id: UUID, db: Session = Depends(get_db)) -> RoomRead:
    """
    Create a PDF for a specific room by ID.

    Args:
        room_id (UUID): The ID of the room to create a PDF for.
        db (Session): The database session.

    Returns:
        RoomRead: The updated RoomRead object with the PDF path.

    Raises:
        HTTPException: If the room is not found or if an unexpected error occurs.
    """
    try:
        existing_room = get_room_or_error(db=db, room_id=room_id, action="PDF creation")

        pdf_name = create_room_pdf(room=existing_room)

        if not pdf_name:
            logger.error(
                f"Failed to create PDF for room with ID {room_id}. No PDF name returned."
            )
            raise HTTPException(
                status_code=500,
                detail="Failed to create PDF for the room",
            )

        # Update the room's PDF path in the database
        room_data = RoomPartialUpdate(pdf=pdf_name)

        room = partial_update_room(
            db=db,
            room_data=room_data,
            room=existing_room,
        )

        return room

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(
            f"An error occurred while creating PDF for room with ID {room_id}: {e}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while creating the PDF",
        )


@router.delete("/{room_id}")
def delete_room(room_id: UUID, db: Session = Depends(get_db)):
    """
    Delete a specific room by ID.

    Args:
        room_id (UUID): The ID of the room to delete.
        db (Session): The database session.

    Raises:
        HTTPException: If the room is not found or if an unexpected error occurs.
    """
    try:
        existing_room = get_room_or_error(db=db, room_id=room_id, action="deletion")

        # Delete the room from the database
        delete_room_entry(db=db, room=existing_room)

        return {"detail": "Room deleted successfully"}

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(
            f"An error occurred while deleting the room with ID {room_id}: {e}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while deleting the room",
        )
