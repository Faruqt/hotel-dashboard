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

    class Config:
        from_attributes = True


class RoomRead(BaseModel):
    """
    Room model representing a room in the system.
    """

    id: UUID
    title: str
    description: str
    image_path: str
    facilities: list[RoomFacilityRead] = []
    created_at_str: str
    updated_at_str: Optional[str] = None

    class Config:
        from_attributes = True


class RoomUpdate(BaseModel):
    """
    Room model for updating room details.
    """

    title: str
    description: Optional[str]
    image: Optional[str]
    facilities: list[str] = []


class RoomReadPaginated(PaginatedResponse):
    """
    Paginated response model for rooms.
    """

    data: list[RoomRead]
