from typing_extensions import Literal
from pydantic import BaseModel, Field


class EntityCustomFieldsBody(BaseModel):
    entityId: str = Field(..., description="实体id", example="xxx")
    entityType: Literal['Resume', 'Job'] = Field(
        default="Resume", description="实体名称", example="Resume"
    )
    payload: dict = Field(..., description="自定义字段的具体内容", example={})
