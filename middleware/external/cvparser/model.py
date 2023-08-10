from typing import Optional
from pydantic import BaseModel, Field


class ParserRequest(BaseModel):
    fileContent: bytes = Field(..., description="文件内容")
    fileName: Optional[str] = Field(default=None, description="文件名", example="xxx")
    parseAvatar: bool = Field(default=True, description="是否解析头像", example=True)
