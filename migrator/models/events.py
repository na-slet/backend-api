import uuid
from datetime import datetime
from enum import Enum

from pytz import UTC
from sqlalchemy import Column, String, TIMESTAMP, INTEGER, ForeignKey, FLOAT, NUMERIC
from sqlalchemy.dialects.postgresql import UUID, ENUM

from .base import DeclarativeBase
from .unions import Unions
from .users import Users


class EventType(str, Enum):
    SCOUT = 'SCOUT'
    TEENAGER = 'TEENAGER'
    JUNIOR = 'JUNIOR'
    FAMILY = 'FAMILY'


class CategoryType(str, Enum):
    EVENT = 'EVENT'
    CAMP = 'CAMP'


class ColorVariant(str, Enum):
    RED = "RED"
    ORANGE = "ORANGE"
    YELLOW = "YELLOW"
    GREEN = "GREEN"
    GRAY = "GRAY"


class LogoVariant(str, Enum):
    SCOUT = "SCOUT"
    CAMP = "CAMP"
    FOREST = "FOREST"
    TRIPLE_DANCING = "TRIPLE_DANCING"
    PAIR_STANDING = "PAIR_STANDING"
    TRIPLE_STANDING = "TRIPLE_STANDING"
    TRIPLE_SITTING = "TRIPLE_SITTING"


class Visibility(str, Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"


class Events(DeclarativeBase):
    __tablename__ = "events"

    id = Column(UUID, unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    short_description = Column(String, nullable=True)
    price = Column(NUMERIC, nullable=True)
    logo_variant = Column(ENUM(LogoVariant), nullable=False)
    visibility = Column(ENUM(Visibility), nullable=False, default=Visibility.PUBLIC)
    city = Column(String, nullable=True)  # TODO: make it enum
    reg_end_date = Column(TIMESTAMP(timezone=True), nullable=False, index=True)
    start_date = Column(TIMESTAMP(timezone=True), nullable=False, index=True)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False, index=True)
    total_places = Column(INTEGER, nullable=True)
    url_link = Column(String, nullable=True)  # social network link
    category_type = Column(ENUM(CategoryType), nullable=False, index=True)
    event_type = Column(ENUM(EventType), nullable=False, index=True)
    union_id = Column(UUID, ForeignKey(Unions.id, ondelete="SET NULL"), nullable=True)
    min_age = Column(INTEGER, nullable=True)
    max_age = Column(INTEGER, nullable=True)
    address = Column(String, nullable=False)
    latitude = Column(FLOAT, nullable=True)  # TODO: make it point
    longitude = Column(FLOAT, nullable=True)
    creator_id = Column(UUID, ForeignKey(Users.id, ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=lambda x: datetime.now(UTC))
    # TODO: add full-text search
