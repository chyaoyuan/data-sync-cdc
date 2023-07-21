# class Table(Base):
#     __tablename__ = 'gleEntity'
#     id = sqlalchemy.Column(sqlalchemy.String(600), primary_key=True)
#     tenant = sqlalchemy.Column(sqlalchemy.String(600))
#     entityType = sqlalchemy.Column(sqlalchemy.String(600), index=True, nullable=False)
#     payload = sqlalchemy.Column(JSONB, nullable=False)
from typing import Literal, Optional

from pydantic import BaseModel, Field


class EntityModel(BaseModel):
    id:  str
    sourceId: str
    tenant: str
    entityType: Literal["Resume", "Job"]
    payload: dict
    extra: Optional[dict] = Field(default={})

