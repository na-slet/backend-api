import uuid
from datetime import datetime

from pytz import UTC
from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID

from .base import DeclarativeBase


class Unions(DeclarativeBase):
    __tablename__ = "unions"

    id = Column(UUID, unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)
    short_name = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=lambda x: datetime.now(UTC))
