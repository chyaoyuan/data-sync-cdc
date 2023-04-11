from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# 邮件本体保存
class EmailBodyInsertModel(BaseModel):
    id: str = Field(..., description="唯一ID 租户+邮箱+邮件")
    body: list[str] = Field(..., description="邮件本体")
    tenant: str = Field(..., description="租户")


class EmailBodyDownloadModel(BaseModel):
    emailUniqueId: str = Field(..., description="唯一ID 租户+邮箱+邮件")

