import uuid
from datetime import datetime
from enum import Enum

from pytz import UTC
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM

from .base import DeclarativeBase
from .unions import Unions


class Roles(str, Enum):
    REGULAR: str = "REGULAR"
    CREATOR: str = "CREATOR"
    ADMIN: str = "ADMIN"


class Genders(str, Enum):
    MALE: str = "male"
    FEMALE: str = "female"


class Users(DeclarativeBase):
    __tablename__ = "users"

    id = Column(UUID, unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    role = Column(ENUM(Roles), nullable=False, default=Roles.REGULAR)
    first_name = Column(String, nullable=True)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    gender = Column(ENUM(Genders), nullable=True)
    phone = Column(String, nullable=True)
    parent_phone = Column(String, nullable=True)
    parent_fio = Column(String, nullable=True)
    parent_email = Column(String, nullable=True)
    email = Column(String, nullable=True, unique=True, index=True)
    city = Column(String, nullable=True)  # TODO: make it enum
    avatar_id = Column(String, default='static/default.png', nullable=False)
    tg_link = Column(String, nullable=True)
    birth_date = Column(TIMESTAMP(timezone=True), nullable=True)
    union_id = Column(UUID, ForeignKey(Unions.id, ondelete="SET NULL"), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=lambda x: datetime.now(UTC))
