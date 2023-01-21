
from uuid import UUID
from enum import Enum
from datetime import datetime, date
from fastapi import Depends, File, UploadFile, Form
from pydantic import BaseModel, Field
from migrations.database.models.events import LogoVariant
from migrations.database.models.events import ColorVariant


class Color(BaseModel):
    type: LogoVariant = Field(None, description='Тип изображения')
    file_id: str = Field(None, description='Ссылка на изображение')


class ColorVariant(BaseModel):
    variant: ColorVariant = Field(..., description='Вариация цвета')
