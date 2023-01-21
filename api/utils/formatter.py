from traceback import format_exception
from typing import Type, TypeVar
from functools import reduce

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def trim_extra_whitespaces(text: str) -> str:
    return " ".join(text.split())


def format_error(error: Exception) -> str:
    if not error:
        return ""
    lines = format_exception(type(error), error, error.__traceback__)
    return "\n".join(lines)


def serialize_models(raw: list[Type], model: Type[T]) -> list[T]:
    return [model.from_orm(elem) for elem in raw]


def __row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d


def combine_models(models: list) -> dict:
    return reduce(lambda a, b: __row2dict(a) | __row2dict(b), models)
