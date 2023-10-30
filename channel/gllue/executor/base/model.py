from typing import Optional

from pydantic import BaseModel, Field


class UrlPath(BaseModel):
    openId: str


class MesoorExtraInUsedConfig(BaseModel):
    urlPath: UrlPath
    # 当存入中央存储，创建、更新、人、时间四个字段要放到headers里
    headers: Optional[dict] = Field(defalut={})
