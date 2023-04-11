from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from emailStorageServer.data_model import ChannelModel, Source


class EmailInfoInsertModel(BaseModel):
    id: str = Field(..., description="唯一ID 租户+邮箱+邮件")
    emailUniqueId: str = Field(..., description="邮件唯一ID")
    tenant: str = Field(..., description="租户")
    channel: ChannelModel = Field(..., description="邮件渠道")
    sender: str = Field(..., description="发件人邮箱")
    fileName: Optional[str] = Field(default=None, description="文件名")
    receiver: str = Field(..., description="收件人邮箱")
    subject: str = Field(..., description="邮件主题")
    html: str = Field(..., description="邮件正文")
    receiveTime: datetime = Field(..., description="邮件时间")
    attachments: Optional[list[dict]] = Field(..., description="附件列表")
    candidateId: Optional[list] = Field(default=[], description="候选人ID")
    candidateUrl: Optional[str] = Field(default=None, description="候选人链接")
    location: Optional[str] = Field(..., description="地点")
    position: Optional[str] = Field(..., description="职位名")
    extra: Optional[dict] = Field(default={}, description="额外字段")
    source: Source = Field(..., description="邮件来源 客户自行上传/协议上传")
    isDelete: bool = Field(default=False, description="软删除标记")


class GetEmailInfoParams(BaseModel):
    id: str = Field(..., description="唯一ID 租户+邮箱+邮件")


class GetEmailAttachmentsParams(BaseModel):
    id: str = Field(..., description="唯一ID 租户+邮箱+邮件")


# 邮件html查询参数
class GetEmailHtmlParams(GetEmailAttachmentsParams):
    pass
