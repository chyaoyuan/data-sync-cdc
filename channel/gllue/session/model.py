from pydantic import BaseModel
from scrapy import Field


class GleUserConfig(BaseModel):
    apiServerHost: str = Field(..., description="客户gllue域名", example="https://www.cgladvisory.com")
    account: str = Field(..., description="谷露权限账号一般是邮箱", example="system@wearecgl.com")
    aesKey: str = Field(..., description="谷露AES密钥", example="ead48dfe1d7cc656")