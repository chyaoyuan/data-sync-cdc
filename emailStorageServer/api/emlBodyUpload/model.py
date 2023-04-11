from typing import Optional, List

from pydantic import BaseModel, Field


class OverWriteConfigModel(BaseModel):
    position: Optional[str] = Field(..., default=None)
    location: Optional[str] = Field(..., default=None)


class OverWriteModel(BaseModel):
    Config: Optional[OverWriteConfigModel] = Field(..., default={})
