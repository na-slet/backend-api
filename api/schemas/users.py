from uuid import UUID
from datetime import date
from uuid import UUID

from fastapi import Form
from pydantic import BaseModel, Field

from migrator.models.users import Genders
from .events import Participation


class UserProfile(BaseModel):
    first_name: str = Form(None, description='Имя пользователя')
    middle_name: str = Form(None, description='Отчество пользователя')
    last_name: str = Form(None, description='Фамилия пользователя')
    gender: Genders = Form(None, description='Пол пользователя')
    phone: str = Form(None, description='Телефон пользователя')
    parent_phone: str = Form(None, description='Телефон родителя')
    parent_fio: str = Form(None, description='ФИО родителя')
    parent_email: str = Form(None, description='Email родителя')
    email: str = Form(None, description='Почта пользователя')
    city: str = Form(None, description='Город пользователя')
    tg_link: str = Form(None, description='Ссылка на Telegram пользователя')
    birth_date: date = Form(None, description='Дата рождения пользователя')
    # avatar: Optional[UploadFile] = File(None, description='Аватарка пользователя')
    union_id: UUID = Form(None, description='UUID объединения')

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    first_name: str = Field(None, description='Имя пользователя')
    middle_name: str = Field(None, description='Отчество пользователя')
    last_name: str = Field(None, description='Фамилия пользователя')
    gender: Genders = Field(None, description='Пол пользователя')
    phone: str = Field(None, description='Телефон пользователя')
    parent_phone: str = Field(None, description='Телефон родителя')
    parent_fio: str = Field(None, description='ФИО родителя')
    parent_email: str = Form(None, description='Email родителя')
    email: str = Field(None, description='Почта пользователя')
    avatar_id: str = Field(None, description='Аватарка пользователя')
    city: str = Field(None, description='Город пользователя')
    tg_link: str = Field(None, description='Ссылка на Telegram пользователя')
    birth_date: date = Field(None, description='Дата рождения пользователя')
    union_id: UUID = Field(None, description='UUID объединения')

    class Config:
        orm_mode = True


class UserParticipation(BaseModel):
    participation: Participation
    user: UserOut