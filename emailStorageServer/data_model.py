import json
from datetime import datetime
from enum import Enum, unique
from typing import Optional, List, Union
from pydantic import BaseModel, Field


# 邮件渠道定义
from utils.custorm_json import DateEncoder


@unique
class ChannelModel(str, Enum):
    """邮件渠道来源：枚举"""
    Job51 = "ehire.51job.com"
    ZhaoPin = "zhaopin.com"
    LPT = "lpt.liepin.com"
    Boss = "zhipin.com"
    City58 = "58.com"
    BJX = "yun.bjx.com.cn"
    Customize = "customize"
    Other = "other"


# 邮件上传方式
@unique
class Source(str, Enum):
    protocol: str = "protocol"
    customer: str = "customer"


class PageParams(BaseModel):
    pageSize: int = Field(default=25, description="页面最大条数")
    pageIndex: int = Field(default=0, description="页码（第N页）")


# 邮件保存类
class EmailModel(BaseModel):
    id: str = Field(..., description="唯一ID 租户+邮箱+邮件")
    emailUniqueId: str = Field(..., description="邮件唯一ID")
    tenant: str = Field(..., description="租户")
    channel: ChannelModel = Field(..., description="邮件渠道")
    sender: str = Field(..., description="发件人邮箱")
    receiver: str = Field(..., description="收件人邮箱")
    subject: str = Field(..., description="邮件主题")
    body: list[str] = Field(..., description="邮件本体")
    html: str = Field(..., description="邮件正文")
    retry: bool = Field(default=False, description="是否为重试邮件")
    retryCount: Optional[int] = Field(default=0, description="手动触发的解析次数")
    receiveTime: datetime = Field(..., description="邮件时间")
    attachments: Optional[list[dict]] = Field(..., description="附件列表")
    candidateId: Optional[list] = Field(default=[], description="候选人ID")
    location: Optional[str] = Field(..., description="地点")
    position: Optional[str] = Field(..., description="职位名")
    extra: Optional[dict] = Field(default={}, description="额外字段")
    source: Source = Field(..., description="邮件来源 客户自行上传/协议上传")
    isDelete: bool = Field(default=False, description="软删除标记")


# 邮件综合查询参数
class GetEmailParams(BaseModel):
    emailUniqueId: Optional[str] = Field(default=None, description="邮件唯一ID")
    emailStartTime: Optional[datetime] = Field(default=None, description="邮件开始时间", examples="1990-01-02")
    emailEndTime: Optional[datetime] = Field(default=None, description="邮件结束时间", examples="2023-01-02")
    tenant: Optional[str] = Field(default=None, description="租户", examples="maisuineiyongceshi")
    channel: Optional[ChannelModel] = Field(default=None, description="邮件渠道")


# 邮件大文件查询参数
class GetEmailAttachmentsParams(BaseModel):
    emailUniqueId: str = Field(description="邮件唯一ID")


# 邮件html查询参数
class GetEmailHtmlParams(GetEmailAttachmentsParams):
    pass


# 内部方便类
class EmailStatusModel(BaseModel):
    retry: bool = Field(default=False, description="是否为重试邮件")
    retryCount: Optional[int] = Field(default=0, description="手动触发的解析次数")
    isDelete: bool = Field(default=False, description="软删除标记")


class RequestDecodeEmailModel(str, Enum):
    Index = "index"
    EmailBodyB64 = "emailBodyB64"
    Tenant = "tenant"
    Email = "email"
    DecodeUUID = "RequestUID"
    LineAttachmentIgnore = "lineAttachmentIgnore"
    ForwardHeaderReplace = "forwardHeaderReplace"


class AttachmentsResponseModel(BaseModel):
    attachmentName: Optional[str] = Field(..., description="附件名称"),
    attachmentFormat: Optional[str] = Field(..., description="附件名称"),
    attachmentBody: Optional[str] = Field(..., description="Base64后的附件body")


class ResponseEmailDecodeModel(BaseModel):
    emailUniqueId: Optional[str] = Field(..., description="邮件唯一ID")
    subject: Optional[str] = Field(..., description="邮件标题/主题")
    receiveTime: Optional[datetime] = Field(..., description="邮件接收时间")
    attachments: List[AttachmentsResponseModel] = Field(..., description="邮件的附件->base64->utf8")
    sender: Optional[str] = Field(..., description="邮件发件人")
    receiver: Optional[str] = Field(..., description="邮件收件人")
    html: Optional[str] = Field(..., description="邮件的html界面")
    position: Optional[str] = Field(..., description="职位名称")
    location: Optional[str] = Field(..., description="工作地点")
    channel: Optional[str] = Field(..., description="渠道")
    candidateLink: Optional[str] = Field(..., description="候选人链接Url")
    requestUID: Optional[str] = Field(..., description="每次请求的唯一ID")


class EmailInfoSketchModel(BaseModel):
    id: Optional[str] = Field(..., description="邮件唯一ID", examples="5f11587107d0c073a7f676f65d4c3215")
    subject: Optional[str] = Field(..., description="邮件标题/主题", examples="【最后3天】邮箱会员6折，仅￥98开通年卡，享10倍存储空间！")
    receiveTime: Optional[datetime] = Field(..., description="邮件接收时间", examples="2022-01-01 00:00:00")


class UpLoadEmlFilesModel(BaseModel):
    exist: list[EmailInfoSketchModel] = Field(description="已存在的邮件")
    insert: list[EmailInfoSketchModel] = Field(description="未存在的邮件")


class UpLoadEmlFilesResponse(BaseModel):
    result: UpLoadEmlFilesModel


class GetEmailInfoResponse(BaseModel):
    id: str = Field(..., description="邮件唯一ID")
    tenant: str = Field(..., description="租户")
    channel: ChannelModel = Field(..., description="邮件渠道")
    sender: str = Field(..., description="发件人邮箱")
    receiver: str = Field(..., description="收件人邮箱")
    subject: str = Field(..., description="邮件主题")
    retryCount: Optional[int] = Field(default=0, description="手动触发的解析次数")
    receiveTime: datetime = Field(..., description="邮件时间")
    candidateId: Optional[list] = Field(default=[], description="候选人ID")
    location: Optional[str] = Field(..., description="地点")
    position: Optional[str] = Field(..., description="职位名")
    source: Source = Field(..., description="邮件来源 客户自行上传/协议上传")


class UpLoadEmlFilesInfo:
    def __init__(self):
        self.body = UpLoadEmlFilesModel(**{
            "exist": [],
            "insert": []
        }).dict()

    def _insert(self, channel: str,  info: EmailInfoSketchModel):
        self.body[channel].append(info.dict())

    def insert_insert(self, info: EmailInfoSketchModel):
        self._insert("insert", info)

    def insert_exist(self, info: EmailInfoSketchModel):
        self._insert("exist", info)

    def result(self):
        return json.loads(json.dumps(self.body, cls=DateEncoder))



