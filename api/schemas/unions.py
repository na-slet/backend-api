
from uuid import UUID

from pydantic import BaseModel, Field


class Union(BaseModel):
    id: UUID = Field(None, description='UUID объединения')
    name: str = Field(None, description='Полное название объединения')
    short_name: str = Field(None, description='Короткое обозначение объединения')

    class Config:
        orm_mode = True