import os
from typing import Optional

import aiohttp
from aiohttp import ClientSession
from loguru import logger
from pydantic import BaseModel, Field


class Settings(BaseModel):
    ResumeSDKServerHost: str
    Authorization: Optional[str] = Field(default="085c11ede59c44588116918f0d3ee1ed")


class ResumeSDKApplication:

    async def parse(self, file_name: str, file_content: str):
        data = {
            "file_name": file_name,
            "file_cont": file_content,
            "need_avatar": 1,
            "ocr_type": 1,
            "need_social_exp": 1,
        }
        data['uid'] = os.getenv("ResumeSDKUID", "2312062")
        data['pwd'] = os.getenv("ResumeSDKPWD", "qHki3cuA2Mm4")
        async with aiohttp.ClientSession() as session:
            res = await session.post("http://www.resumesdk.com/api/parse", ssl=False, json=data)
            if res.status == 200:
                response_info = await res.json()
                return response_info.get("result", {})
            logger.error(res.status)
            logger.error(await res.text())
            return None