from datetime import datetime, date
from typing import Optional
from uuid import UUID

from fastapi import File, UploadFile
from pydantic import BaseModel, Field

from api.schemas.unions import Union
from database.models.events import CategoryType, EventType, LogoVariant
from database.models.events import Visibility
from database.models.participations import ParticipationStages


class EventSearch(BaseModel):
    reg_start_date: date = Field(None, description='Начальная дата промежутка поиска')
    reg_end_date: date = Field(None, description='Конечная дета промежутка поиска')
    start_date: date = Field(None, description='Начальная дата промежутка поиска')
    end_date: date = Field(None, description='Конечная дата промежутка поиска')
    category_type: CategoryType = Field(None, description='Категория слёта')
    event_type: EventType = Field(None, description='Тип слёта')
    query: str = Field(None, description='Поисковый запрос')


class UserEventUpdate(BaseModel):
    event_id: UUID
    user_id: UUID
    stage: ParticipationStages

class UserEvent(BaseModel):
    stage: ParticipationStages


class EventOut(BaseModel):
    id: UUID = Field(None, description='UUID слёта')
    name: str = Field(None, description='Название слёта')
    description: str = Field(None, description='Описание слёта')
    short_description: str = Field(None, description='Короткое описание слёта')
    visibility: Visibility = Field(None, description='Видимость слёта')
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


class FoundEvent(BaseModel):
    event: EventOut
    union: Union
    participation: Optional[Participation]


class UserRequiredAdult(BaseModel):
    first_name: str = Field(..., description='Имя пользователя')
    middle_name: str = Field(..., description='Отчество пользователя')
    last_name: str = Field(..., description='Фамилия пользователя')
    phone: str = Field(..., description='Телефон пользователя')
    email: str = Field(..., description='Почта пользователя')
    city: str = Field(..., description='Город пользователя')
    birth_date: date = Field(..., description='Дата рождения пользователя')
    union_id: UUID = Field(..., description='UUID объединения')

    class Config:
        orm_mode = True


class UserRequiredChild(UserRequiredAdult):
    parent_phone: str = Field(..., description='Телефон родителя')
    parent_fio: str = Field(..., description='ФИО родителя')

    class Config:
        orm_mode = True

class UserParticipation(BaseModel):
    participation: Participation
    event: EventOut

class UserEventKick(BaseModel):
    event_id: UUID
    user_id: UUID


class EventInOptional(BaseModel):
    id: Optional[UUID]


class EventNew(BaseModel):
    name: str = Field(..., description='Название слёта')
    description: str = Field(None, description='Описание слёта')
    short_description: str = Field(None, description='Короткое описание слёта')
    visibility: Visibility = Field(None, description='Видимость слёта')
    price: float = Field(None, description='Цена участия на слёте',gt=0)
    logo_variant: LogoVariant = Field(..., description='Вариант логотипа')
    city: str = Field(None, description='Локация слёта')
    reg_end_date: datetime = Field(..., description='Окончание регистрации')
    start_date: datetime = Field(..., description='Начало слёта')
    end_date: datetime = Field(..., description='Конец слёта')
    total_places: int = Field(None, description='Количество мест')
    url_link: str = Field(None, description='Ссылка на соц. сети')
    event_type: EventType = Field(..., description='Тип слёта')
    category_type: CategoryType = Field(..., description='Категория слёта')
    union_id: UUID = Field(None, description='UUID объединения')
    min_age: int = Field(None, gt=0, description='Минимальный возраст')
    max_age: int = Field(None, gt=0, description='Максимальный возраст')
    address: str = Field(..., description='Адрес слёта')
    latitude: float = Field(None, description='Широта места слёта')
    longitude: float = Field(None, description='Долгота места слёта')

