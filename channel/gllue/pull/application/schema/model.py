from enum import Enum
from typing import Literal, Union

from pydantic import BaseModel, Extra


class Entity(Enum):
    Candidate = "Candidate"
    Position = "Position"


class GleFieldType(str,Enum):
    foreignkey = "foreignkey"
    char = "char"
    boolean = "boolean"
    integer = "integer"
    text = "text"
    date = "date"
    decimal = "decimal"


class SchemaFieldInfo(BaseModel, extra=Extra.allow):
    """schema的每个字段详情"""
    name: str
    type: GleFieldType


