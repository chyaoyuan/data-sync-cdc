from pydantic import BaseModel, Field


class ConnectionInsertModel(BaseModel):
    ms_entity_type: str = Field(..., description="")
    open_id: str = Field(..., description="麦穗系统中的ID")
    tenant: str = Field(..., description="租户")

    source_id: str = Field(..., description="entity表的ID")
    is_delete: bool = Field(...)


class SearchAttachmentModel(BaseModel):
    openId: str = Field(..., description="")
    tenant: str = Field(..., description="租户")




