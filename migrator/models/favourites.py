import uuid
from datetime import datetime

from pytz import UTC
from sqlalchemy import Column, TIMESTAMP, ForeignKey, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID

from .base import DeclarativeBase
from .events import Events
from .users import Users


class Favourites(DeclarativeBase):
    __tablename__ = "favourites"

    id = Column(UUID, unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(UUID, ForeignKey(Users.id, ondelete="CASCADE"), nullable=False, index=True)
    event_id = Column(UUID, ForeignKey(Events.id, ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=lambda x: datetime.now(UTC))

    __table_args__ = (UniqueConstraint("user_id", "event_id"),)


Index('favourites_user_event_idx', Favourites.user_id, Favourites.event_id)
