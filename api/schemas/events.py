
from uuid import UUID
from enum import Enum
from datetime import datetime, date
from fastapi import Depends, File, UploadFile, Form
from pydantic import BaseModel, Field
from migrations.database.models.participations import ParticipationStages


class EventSearch(BaseModel):
    start_date: date = Field(..., description='Начальная дата промежутка поиска')
    end_date: date = Field(None, description='Конечная дата промежутка поиска')
    query: str = Field(None, description='Поисковый запрос')

class UserEvent(BaseModel):
    stage: ParticipationStages = Field(..., description='Стадия принятия на слёт')

class EventOut(BaseModel):
    name: str = Field(None, description='Название слёта')
    description: str = Field(None, description='Описание слёта')
    city: str = Field(None, description='Локация слёта')
    start_date: datetime = Field(None, description='Начало слёта')
    end_date: datetime = Field(None, description='Конец слёта')
    total_places: int = Field(None, description='Количество мест')
    url_link: str = Field(None, description='Ссылка на соц. сети')
    address: str = Field(None, description='Адрес слёта')
    logo_id: str = Field(None, description='Ссылка на логотип слёта')