# library imports
import uuid
from datetime import datetime
from sqlalchemy import event, Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

# local imports
from app.database.base import Base
from app.config.settings import APP_URL, IMAGE_DIR, PDF_DIR, DATE_OUTPUT_FORMAT


class Room(Base):
    """
    Room model representing a room in the database.
    Inherits from the SQLAlchemy Base class.
    """

    __tablename__ = "rooms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, index=True, nullable=False, unique=True)
    description = Column(String)
    image = Column(String)
    pdf = Column(String)
    facilities = relationship(
        "RoomFacility",
        backref="room",
        cascade="all, delete-orphan",
    )
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime)

    def _format_date(self, dt):
        return dt.strftime(DATE_OUTPUT_FORMAT) if dt else None

    @property
    def image_path(self):
        """Return the full URL for the room image."""
        return f"{APP_URL}/{IMAGE_DIR}/{self.image}" if self.image else None

    @property
    def pdf_path(self):
        """Return the full URL for the room PDF."""
        return f"{APP_URL}/{PDF_DIR}/{self.pdf}" if self.pdf else None

    @property
    def facilities_list(self):
        """
        Return a list of facility names associated with the room.
        """
        return (
            [facility.facility_name for facility in self.facilities]
            if self.facilities
            else []
        )

    @property
    def facilities_count(self):
        """
        Return the count of facilities associated with the room.
        """
        return len(self.facilities) if self.facilities else 0

    @property
    def created_at_str(self):
        """Return the created_at date as a string."""
        return self._format_date(self.created_at)

    @property
    def updated_at_str(self):
        """Return the updated_at date as a string."""
        return self._format_date(self.updated_at)

    def __repr__(self):
        return f"<Room id={self.id} title={self.title}>"


class RoomFacility(Base):
    """
    RoomFacility model representing a facility associated with a room.
    Inherits from the SQLAlchemy Base class.
    """

    __tablename__ = "room_facilities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    facility_name = Column(String, index=True)
    room_id = Column(
        UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="CASCADE"), index=True
    )
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"<RoomFacility id={self.id} facility_name={self.facility_name}>"


@event.listens_for(Room, "before_update")
@event.listens_for(RoomFacility, "before_update")
def update_timestamp(mapper, connection, target):
    """Update timestamp before model update."""
    target.updated_at = datetime.now()
