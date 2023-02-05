import uuid
from datetime import datetime
from enum import Enum

from pytz import UTC
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID, ENUM

from .base import DeclarativeBase
from .users import Users


class CredentialTypes(str, Enum):
    BASIC: str = 'BASIC'
    VK: str = 'VK'
    GOOGLE: str = 'GOOGLE'


class Credentials(DeclarativeBase):
    __tablename__ = "credentials"

    id = Column(UUID, unique=True, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(UUID, ForeignKey(Users.id, ondelete="CASCADE"), nullable=False, index=True)
    credential_type = Column(ENUM(CredentialTypes), nullable=False, default=CredentialTypes.BASIC)
    value = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=lambda x: datetime.now(UTC))

    __table_args__ = (
        UniqueConstraint(user_id, credential_type),
    )


Index('credentials_user_credential_type_idx', Credentials.user_id, Credentials.credential_type)
