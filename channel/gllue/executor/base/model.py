from typing import Optional

from pydantic import BaseModel, Field


class UrlPath(BaseModel):
    openId: str

# 配置化写入Tip


class MesoorExtraInUsedConfig(BaseModel):
    urlPath: UrlPath
    # 当存入中央存储，创建、更新、人、时间四个字段要放到headers里
    headers: Optional[dict] = Field(defalut={})
    putStatus: Optional[int] = Field(default=None, description="会先get一下，如果返回code一致才put")
