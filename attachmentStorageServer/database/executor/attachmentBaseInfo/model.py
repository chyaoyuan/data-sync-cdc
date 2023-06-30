from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
#     # openId = Column(String(600), primary_key=True, index=True, comment="自增长")
#     #     tenant = Column(String(600), nullable=False, comment="租户")
#     #     isDelete = Column(BOOLEAN, comment="软删除")
#     #     createAt = Column(DateTime, server_default=func.now(), comment="创建时间")
#     #     updateAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")


class AttachmentBodyInsertModel(BaseModel):
    openId: str = Field(..., description="")
    tenant: str = Field(..., description="租户")
    isDelete: bool = Field(...)


class SearchAttachmentModel(BaseModel):
    openId: str = Field(..., description="")
    tenant: str = Field(..., description="租户")



