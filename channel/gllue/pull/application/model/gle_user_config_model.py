from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class GleUserConfig(BaseModel):
    apiServerHost: str = Field(..., description="客户gllue域名", example="https://www.cgladvisory.com")
    account: str = Field(..., description="谷露权限账号一般是邮箱", example="system@wearecgl.com")
    aesKey: str = Field(..., description="谷露AES密钥", example="ead***1d7**656")
    # 以下账户
    extraPassword: Optional[str] = Field(default="", description="谷露前端登陆密码，当aes没有权限访问对应接口时的备份")
    extraAccount: Optional[str] = Field(default="", description="谷露前端登陆账户")