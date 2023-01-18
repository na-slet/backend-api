
from uuid import UUID
from enum import Enum
from datetime import date
from fastapi import Depends, File, UploadFile, Form
from pydantic import BaseModel, Field
from migrations.database.models.users import Genders
from migrations.database.models.credentials import CredentialTypes


class UserUpdate(BaseModel):
    first_name: str = Form(None, description='Имя пользователя')
    last_name: str = Form(None, description='Фамилия пользователя')
    phone: str = Form(None, description='Телефон пользователя')
    gender: Genders = Form(None, description='Пол пользователя')
    avatar: UploadFile = File(None, description='Аватарка пользователя')
    city: str = Form(None, description='Город пользователя')
    tg_link: str = Form(None, description='Ссылка на Telegram пользователя')
    birth_date: date = Form(None, description='Дата рождения пользователя')


class UserRegister(BaseModel):
    email: str = Form(..., description='Email пользователя')
    password: str = Form(..., description='Пароль пользователя')


class UserLoginBasic(BaseModel):
    identity: str = Form(..., description='Email или телефон пользователя')
    password: str = Form(..., description='Пароль пользователя')


class UserLoginOAuth2(BaseModel):
    credential_type: CredentialTypes = Form(..., description='Тип авторизации')
