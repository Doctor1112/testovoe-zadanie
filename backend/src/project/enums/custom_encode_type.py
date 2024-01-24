from enum import auto

from project.enums import NameEnum


class CustomEncodeType(NameEnum):
    TORTOISE = auto()
    PYDANTIC = auto()
    ENUM = auto()
