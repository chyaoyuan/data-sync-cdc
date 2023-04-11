from enum import unique, Enum
from typing import List

from pydantic import BaseModel, Field


class EmailDecodeServerRequest(BaseModel):
    emailBodyB64: List[str] = Field(..., description="经过base64再decode(utf8)的邮件本体")
    RequestUID: str = Field(..., description="每次解码请求对应的唯一ID")
    lineAttachmentIgnore: bool = Field(..., description="是否忽略正文内的附件(实验功能)")
    forwardHeaderReplace: bool = Field(..., description="是否去除正文内转发邮件头(实验功能)")
