# library imports
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

# local imports
from app.schemas.base import PaginatedResponse


class RoomCreate(BaseModel):
    """
    Room model for creating a new room.
    """

    title: str
    description: str
    image: str
    facilities: list[str] = []


class RoomFacilityRead(BaseModel):
    """
    RoomFacility model representing a facility in a room.
    """

    id: UUID
    facility_name: str

    class ConfigDict:
        from_attributes = True


class BaseRoomRead(BaseModel):
    """
    Room model representing a room in the system.
    """

    id: UUID
    title: str
    description: str
    facilities_count: Optional[int] = None
    created_at_str: str
    updated_at_str: Optional[str] = None


class RoomRead(BaseRoomRead):
    """
    Room model for reading room details.
    """

    facilities_list: list[str] = []
    image_path: str
    pdf_path: Optional[str]

    class ConfigDict:
        from_attributes = True


class RoomCompleteUpdate(BaseModel):
    """
    Room model for updating room details.
    """

    title: str
    description: Optional[str]
    image: Optional[str]
    facilities: list[str] = []


class RoomPartialUpdate(BaseModel):
    """
    Room model for partially updating room details.
    """

    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    pdf: Optional[str] = None
    facilities: Optional[list[str]] = None


class RoomReadPaginated(PaginatedResponse):
    """
    Paginated response model for rooms.
    """

    data: list[BaseRoomRead]

    class ConfigDict:
        from_attributes = True
