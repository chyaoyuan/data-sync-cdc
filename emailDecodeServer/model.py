from enum import unique, Enum
from typing import List

from pydantic import BaseModel, Field


class EmailDecodeServerRequest(BaseModel):
    emailBodyB64: List[str] = Field(..., description="经过base64再decode(utf8)的邮件本体")
    RequestUID: str = Field(..., description="每次解码请求对应的唯一ID")
    lineAttachmentIgnore: bool = Field(..., description="是否忽略正文内的附件(实验功能)")
    forwardHeaderReplace: bool = Field(..., description="是否去除正文内转发邮件头(实验功能)")
    tenant: str = Field(..., description="租户")


@unique
class ChannelModel(str, Enum):
    """邮件渠道来源：枚举"""
    Job51 = "ehire.51job.com"
    ZhaoPin = "zhaopin.com"
    LPT = "lpt.liepin.com"
    Boss = "zhipin.com"
    City58 = "58.com"
    BJX = "yun.bjx.com.cn"
    DIY = "diy"
    Other = "other"