
from uuid import UUID
from enum import Enum
from datetime import date
from fastapi import Depends, File, UploadFile, Form
from pydantic import BaseModel, Field
from migrations.database.models.users import Genders


class Union(BaseModel):
    id: UUID = Field(None, description='UUID объединения')
    name: str = Field(None, description='Полное название объединения')
    short_name: str = Field(None, description='Короткое обозначение объединения')

    class Config:
        orm_mode = True