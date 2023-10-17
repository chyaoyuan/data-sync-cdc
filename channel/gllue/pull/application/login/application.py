import asyncio
import json

import aiohttp
from loguru import logger

from channel.gllue.pull.application.base.application import BaseApplication


class LoginInApp(BaseApplication):
    def __init__(self, gle_user_config: dict):
        super().__init__(gle_user_config)

    async def login_in_gle(self):
        fd = aiohttp.FormData()
        sttt = json.dumps({
                         "password": self.gle_user_config.extraPassword,
                         "remember": True,
                         "next": "/",
                         "email": self.gle_user_config.extraAccount,
                         "lang": "zh_CN"}, ensure_ascii=False)
        print(sttt)
        fd.add_field("data", sttt)

        _ = await self.normal_session.post(f"{self.gle_user_config.apiServerHost}/rest/user/login", data=fd,
                                           func=self.request_cookies_callback)
        print(_.get("uid").value)
        logger.info(_.output)
        logger.info(list(dir(_)))
        logger.info(type(_))


if __name__ == '__main__':
    asyncio.run(LoginInApp({
        "apiServerHost": "https://www.cgladvisory.com",
        "aesKey": "398b5ec714c59be2",
        "account": "system@wearecgl.com",

        "extraAccount": "luyi@mesoor.com",
        "extraPassword": "2zp0wz42"
    }).login_in_gle())
