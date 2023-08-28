from typing import Literal, List

from pydantic import BaseModel, Field


class GleUserConfig(BaseModel):
    apiServerHost: str = Field(..., description="客户gllue域名", example="https://www.cgladvisory.com")
    account: str = Field(..., description="谷露权限账号一般是邮箱", example="system@wearecgl.com")
    aesKey: str = Field(..., description="谷露AES密钥", example="ead48dfe1d7cc656")


class EntityConvertModel(BaseModel):
    tenantAlias: str
    openId: str
    entityType: str
    body: dict
    convertBody: dict


class GlePushEntityModel(BaseModel):
    entityBodyList: List[EntityConvertModel] = Field(description="谷露实体，格式严格按照谷露schema，因为谷露可以自定义schema，每个客户的schema会有所不同")
    GleUserConfig: GleUserConfig = Field(description="谷露的用户配置")

