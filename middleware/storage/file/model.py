from typing import Optional
from pydantic import BaseModel, Field


class SaveFileBody(BaseModel):
    fileContent: bytes = Field(..., description="文件内容 二进制形式")
    fileName: str = Field(..., description="文件名", example="xxx.pdf")
    key: Optional[str] = Field(default=None, description="文件的key", example="xxx")


class SaveB64FileBody(SaveFileBody):
    fileContent: str = Field(..., description="文件内容 base64形式")
