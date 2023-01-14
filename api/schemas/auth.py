
from uuid import UUID
from enum import Enum
from datetime import date
from fastapi import Depends, File, UploadFile, Form
from pydantic import BaseModel, Field
from migrations.database.models.users import Genders
from migrations.database.models.credentials import CredentialTypes

class UserRegister(BaseModel):
    first_name: str = Form(..., description='Имя пользователя')
    last_name: str = Form(..., description='Фамилия пользователя')
    gender: Genders = Form(..., description='Пол пользователя')
    phone: str = Form(..., description='Телефон пользователя')
    email: str = Form(..., description='Почта пользователя')
    password: str = Form(..., description='Пароль пользователя')
    avatar: UploadFile = File(..., description='Аватарка пользователя')
    tg_link: str = Form(..., description='Ссылка на Telegram пользователя')
    birth_date: date = Form(..., description='Дата рождения пользователя')

class UserLoginBasic(BaseModel):
    identity: str = Form(..., description='Email или телефон пользователя')
    password: str = Form(..., description='Пароль пользователя')

class UserLoginOAuth2(BaseModel):
    credential_type: CredentialTypes = Form(..., description='Тип авторизации')
