from typing import Optional

from pydantic import BaseModel, Field


class EmailLogInsertModel(BaseModel):
    id: str = Field(..., description="唯一ID 租户+邮箱+邮件")
    retryCount: Optional[int] = Field(default=0, description="手动触发的解析次数")
    retryExtra: Optional[dict] = Field(default={}, description="额外字段")


