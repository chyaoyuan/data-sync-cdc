from pydantic import BaseModel, Field


class EntityInsertModel(BaseModel):
    entity_type: str = Field(..., description="")
    source_id: str = Field(..., description="租户")
    tenant: str = Field(..., description="租户")
    is_delete: bool = Field(...)
    payload: dict = Field(...)


class SearchEntityModel(BaseModel):
    entity_type: str = Field(..., description="")
    source_id: str = Field(..., description="租户")
    tenant: str = Field(..., description="租户")
    is_delete: bool = Field(...)


