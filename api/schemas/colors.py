from enum import Enum

from pydantic import BaseModel, Field

from database.models.events import LogoVariant
from database.models.participations import ParticipationStages


class ColorVariants(str, Enum):
    RED = "RED"
    ORANGE = "ORANGE"
    YELLOW = "YELLOW"
    GREEN = "GREEN"
    GRAY = "GRAY"


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
