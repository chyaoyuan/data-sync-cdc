from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class GleURL:
    def __init__(self, apiServerHost: str):
        # 一般用于测试token有效性
        self.candidate_simple_list_with_ids_url: str = "{apiServerHost}/rest/candidate/simple_list_with_ids".format(apiServerHost=apiServerHost)
        self.check = "{apiServerHost}/rest/joborder/simple_list_with_ids".format(apiServerHost=apiServerHost)


class GleUserConfig(BaseModel):
    apiServerHost: str = Field(..., description="客户gllue域名", example="https://www.cgladvisory.com")
    account: str = Field(..., description="谷露权限账号一般是邮箱", example="system@wearecgl.com")
    aesKey: str = Field(..., description="谷露AES密钥", example="ead48dfe1d7cc656")


class BaseResponseModel(BaseModel):
    ids: list = Field(..., description="ID列表")
    currentpage: int = Field(...,description="当前页码")
    totalcount: int = Field(..., description="rows总量")
    totalpages: int = Field(...,description="总页数")
    result: Optional[dict]
