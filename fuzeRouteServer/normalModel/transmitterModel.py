from pydantic import BaseModel


class TransmitterRequestModel(BaseModel):
    tenantAlias: str
    openId: str
    entityType: str


class EntityModel(BaseModel):
    tenantAlias: str
    openId: str
    entityType: str
    body: dict


class EntityConvertModel(BaseModel):
    tenantAlias: str
    openId: str
    entityType: str
    body: dict
    convertBody: dict
