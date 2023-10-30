import asyncio
import http.cookies
from typing import Optional
import aiohttp
from channel.gllue.pull.application.base.model import GleUrlConfig
from channel.gllue.pull.application.model.gle_user_config_model import GleUserConfig
from channel.gllue.session.normal_session import HoMuraSession
from utils.logger import logger
from channel.gllue.session.gllue_aiohttp_session import GlHoMuraSession


class BaseApplication:
    def __init__(self, gle_user_config: dict):
        self.settings = GleUrlConfig
        self.gle_user_config: GleUserConfig = GleUserConfig(**gle_user_config)
        self.async_session: GlHoMuraSession = GlHoMuraSession(
            client_session=aiohttp.ClientSession, gle_user_config=self.gle_user_config.dict(), retry_when=lambda x: not isinstance(x, asyncio.exceptions.TimeoutError)
        )

    @staticmethod
    async def request_response_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            raise Exception(f"{res.status} {await res.text()} {res.url}")
        _ = await res.json()
        return await res.json(), res.status

    @staticmethod
    async def status_check_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            return await res.text(), res.status
        if res.status == 200:
            response = await res.json()
            if "status" in response.keys():
                raise Exception(f"res->{response}")

        return await res.json(), res.status

    @staticmethod
    async def request_file_response_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            return await res.text(), res.status
        return await res.content.read(), res.headers

    @staticmethod
    def pop_useless_params(params: dict):
        return {k: v for k, v in params.items() if v}

    @staticmethod
    async def request_cookies_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            raise Exception(f"{res.status} {await res.text()}")
        info = await res.json()
        if not info.get("status"):
            raise Exception(f"登陆失败->{info}")
        return res.cookies


if __name__ == '__main__':
    pass
    b = BaseApplication(
        {
            "apiServerHost": "https://fsgtest.gllue.net",
            "aesKey": "824531e8cad2a287",
            "account": "api@fsg.com.cn"
        }
    )



