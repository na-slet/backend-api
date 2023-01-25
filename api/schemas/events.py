
from uuid import UUID
from enum import Enum
from datetime import datetime, date
from fastapi import Depends, File, UploadFile, Form
from pydantic import BaseModel, Field
from migrations.database.models.participations import ParticipationStages
from migrations.database.models.events import CategoryType, EventType, LogoVariant
from api.schemas.unions import Union


class EventSearch(BaseModel):
    reg_start_date: date = Field(None, description='Начальная дата промежутка поиска')
    reg_end_date: date = Field(None, description='Конечная дета промежутка поиска')
    start_date: date = Field(None, description='Начальная дата промежутка поиска')
    end_date: date = Field(None, description='Конечная дата промежутка поиска')
    category_type: CategoryType = Field(None, description='Категория слёта')
    event_type: EventType = Field(None, description='Тип слёта')
    query: str = Field(None, description='Поисковый запрос')


class UserEvent(BaseModel):
    stage: ParticipationStages = Field(..., description='Стадия принятия на слёт')


class EventOut(BaseModel):
    id: UUID = Field(None, description='UUID слёта')
    name: str = Field(None, description='Название слёта')
    description: str = Field(None, description='Описание слёта')
    short_description: str = Field(None, description='Короткое описание слёта')
    price: float = Field(None, description='Цена участия на слёте')
    logo_variant: LogoVariant = Field(None, description='Вариант логотип')
    city: str = Field(None, description='Локация слёта')
    reg_end_date: datetime = Field(None, description='Окончание регистрации')
    start_date: datetime = Field(None, description='Начало слёта')
    end_date: datetime = Field(None, description='Конец слёта')
    total_places: int = Field(None, description='Количество мест')
    url_link: str = Field(None, description='Ссылка на соц. сети')
    event_type: EventType = Field(None, description='Тип слёта')
    category_type: CategoryType = Field(None, description='Категория слёта')
    union_id: UUID = Field(None, description='UUID объединения')
    min_age: int = Field(None, gt=0, description='Минимальный возраст')
    max_age: int = Field(None, gt=0, description='Максимальный возраст')
    address: str = Field(None, description='Адрес слёта')
    latitude: float = Field(None, description='Широта места слёта')
    longitude: float = Field(None, description='Долгота места слёта')

    class Config:
        orm_mode = True


class FoundEvent(BaseModel):
    event: EventOut
    union: Union


class EventIn(BaseModel):
    id: UUID = Field(..., description='UUID слёта')


class PaymentPhoto(BaseModel):
    event_id: UUID = Field(..., description='UUID слёта')
    payment: UploadFile = File(None, description='Скрин об оплате')


class Participation(BaseModel):
    participation_stage: ParticipationStages = Field(None, description='Стадия принятия на слёт')
    payment_id: str = Field(None, description='Скрин об оплате')

    class Config:
        orm_mode = True


class UserParticipation(BaseModel):
    participation: Participation
    event: EventOut
