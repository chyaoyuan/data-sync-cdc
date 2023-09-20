from typing import Literal, List, Optional

from pydantic import BaseModel, Field


class GleUserConfig(BaseModel):
    apiServerHost: str = Field(..., description="客户gllue域名", example="https://www.cgladvisory.com")
    account: str = Field(..., description="谷露权限账号一般是邮箱", example="system@wearecgl.com")
    aesKey: str = Field(..., description="谷露AES密钥", example="ead48dfe1d7cc656")


class EntityModel(BaseModel):
    sourceEntityType: Literal["jobOrder", "client", "jobSubMission", "candidate"]
    sourceId: Optional[str]
    data: dict


class FieldConfig(BaseModel):
    fieldJMESPath: str
    fieldName: str


class EntityExtractConfig(BaseModel):
    entityName: Literal["jobOrder", "client", "jobSubMission", "candidate"]
    fieldCConfig: List[FieldConfig]


class GlePushEntityModel(BaseModel):
    entityBodyList: List[EntityModel] = Field(description="谷露实体，格式严格按照谷露schema，因为谷露可以自定义schema，每个客户的schema会有所不同")
    gleUserConfig: GleUserConfig = Field(description="谷露的用户配置")
    entityConfigMap: Optional[List[EntityExtractConfig]] = Field(default=None, description="字段抽取规则")


