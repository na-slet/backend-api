
from uuid import UUID

from fastapi import Depends, File, UploadFile, Form
from pydantic import BaseModel, Field
from migrations.database.models.users import Gender, Users



class UserIn(BaseModel):
    email: str = Form(..., description="Почта пользователя")
    gender: Gender = Form(None, description="Пол пользователя")
    name: str = Form(None, description="Имя пользователя")
    surname: str = Form(None, description="Фамилия пользователя")