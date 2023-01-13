from dataclasses import asdict
from traceback import format_exception
from typing import Type, TypeVar

from pydantic import BaseModel


def trim_extra_whitespaces(text: str) -> str:
    return " ".join(text.split())


def format_error(error: Exception) -> str:
    if not error:
        return ""
    lines = format_exception(type(error), error, error.__traceback__)
    return "\n".join(lines)