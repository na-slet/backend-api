
from uuid import UUID
from enum import Enum
from datetime import datetime, date
from fastapi import Depends, File, UploadFile, Form
from pydantic import BaseModel, Field
from migrations.database.models.events import LogoVariant
from migrations.database.models.participations import ParticipationStages


class ColorStages(str, Enum):
    NOT_PARTICIPATED = 'NOT_PARTICIPATED'
    PAYMENT_NEEDED: str = "PAYMENT_NEEDED"
    PAYMENT_PENDING: str = "PAYMENT_PENDING"
    APPROVED: str = "APPROVED"
    DECLINED: str = "DECLINED"


class Color(BaseModel):
    type: LogoVariant = Field(None, description='Тип изображения')
    file_id: str = Field(None, description='Ссылка на изображение')


class ColorStage(BaseModel):
    stage: ParticipationStages = Field(..., description='Стадия участия')
