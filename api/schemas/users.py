
from uuid import UUID
from enum import Enum
from datetime import date
from fastapi import Depends, File, UploadFile, Form
from pydantic import BaseModel, Field
from migrations.database.models.users import Genders


class UserProfile(BaseModel):
    first_name: str = Form(None, description='Имя пользователя')
    last_name: str = Form(None, description='Фамилия пользователя')
    gender: Genders = Form(None, description='Пол пользователя')
    phone: str = Form(None, description='Телефон пользователя')
    email: str = Form(None, description='Почта пользователя')
    avatar: UploadFile = File(None, description='Аватарка пользователя')
    city: str = Form(None, description='Город пользователя')
    tg_link: str = Form(None, description='Ссылка на Telegram пользователя')
    birth_date: date = Form(None, description='Дата рождения пользователя')

    class Config:
        orm_mode = True