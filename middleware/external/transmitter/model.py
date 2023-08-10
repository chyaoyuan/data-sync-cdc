from typing import Optional

from pydantic import BaseModel, Field


class SaveDataRequest(BaseModel):
    tenant: str = Field(..., description="租户", example="mesoor-98")
    entityType: str = Field(..., description="实体类型", example="ApplicantStandardResume")
    entityId: str = Field(..., description="实体id", example="xxx")
    entity: dict = Field(..., description="实体内容", example={})
    source: str = Field(..., description="来源", example="xxx")
    editor: str = Field(default=None, description="编辑者", example="xxx")
    schema_id: Optional[str] = Field(default=None, description="schema", example="xxx")


class GetDataRequest(BaseModel):
    tenant: str = Field(..., description="租户", example="mesoor-98")
    entityType: str = Field(..., description="实体类型", example="ApplicantStandardResume")
    entityId: str = Field(..., description="实体id", example="xxx")


class DeleteEntityRequest(GetDataRequest):
    source: str = Field(default="sg", description="来源", example="xxx")
    editor: str = Field(default="sg", description="编辑者", example="xxx")
