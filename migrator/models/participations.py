import uuid
from datetime import datetime
from enum import Enum

from pytz import UTC
from sqlalchemy import Column, TIMESTAMP, ForeignKey, UniqueConstraint, String, Index
from sqlalchemy.dialects.postgresql import UUID, ENUM

from .base import DeclarativeBase
from .events import Events
from .users import Users


class ParticipationStages(str, Enum):
    NOT_PARTICIPATED: str = "NOT_PARTICIPATED"
    PAYMENT_NEEDED: str = "PAYMENT_NEEDED"
    PAYMENT_PENDING: str = "PAYMENT_PENDING"
    APPROVED: str = "APPROVED"
    DECLINED: str = "DECLINED"


class Participations(DeclarativeBase):
    __tablename__ = "participations"

    id = Column(UUID, unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(UUID, ForeignKey(Users.id, ondelete="CASCADE"), nullable=False, index=True)
    event_id = Column(UUID, ForeignKey(Events.id, ondelete="CASCADE"), nullable=False, index=True)
    participation_stage = Column(ENUM(ParticipationStages), nullable=False, default=ParticipationStages.PAYMENT_NEEDED)
    payment_id = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=lambda x: datetime.now(UTC))

    __table_args__ = (UniqueConstraint("user_id", "event_id"),)


Index('participations_user_event_idx', Participations.user_id, Participations.event_id)
