from pydantic import BaseModel

class UrlPath(BaseModel):
    openId: str


class MesoorExtraInUsedConfig(BaseModel):
    urlPath: UrlPath
