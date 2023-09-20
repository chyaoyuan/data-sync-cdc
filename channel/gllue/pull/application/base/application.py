import asyncio
from typing import Optional

import aiohttp
from utils.logger import logger

from channel.gllue.pull.application.base.model import GleURL, GleUserConfig
from channel.gllue.session.gllue_aiohttp_session import GlHoMuraSession


class GleUrlConfig:
    get_entity_url = "/rest/{entityType}/simple_list_with_ids"
    get_entity_schema_url = "/rest/custom_field/{entityType}"
    # 系统参数的数据字典(来自文档)
    get_system_model_url = "/rest/custom_field/{entityType}/list"
    # 参数字典(来自前端)
    get_field_schema_url = "/rest/{entityType}/list"
    #


class BaseApplication:
    def __init__(self, gle_user_config: dict):
        self.settings = GleUrlConfig
        self.gle_user_config: GleUserConfig = GleUserConfig(**gle_user_config)
        self.gle_url = GleURL(GleUserConfig(**gle_user_config).apiServerHost)

        self.async_session: GlHoMuraSession = GlHoMuraSession(
            client_session=aiohttp.ClientSession, gle_user_config=self.gle_user_config.dict(), retry_when=lambda x: not isinstance(x, asyncio.exceptions.TimeoutError)
        )

    @staticmethod
    async def request_response_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            raise Exception(f"{res.status} {await res.text()}")
            # return await res.text(), res.status
        return await res.json(), res.status

    @staticmethod
    async def status_check_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            return await res.text(), res.status
        if res.status == 200:
            response = await res.json()
            logger.info(response)
            if "status" in response.keys():
                raise Exception(f"res->{response}")

        return await res.json(), res.status

    @staticmethod
    async def request_file_response_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            return await res.text(), res.status
        return await res.content.read(), res.headers


if __name__ == '__main__':
    pass
    b = BaseApplication(
        {
            "apiServerHost": "https://fsgtest.gllue.net",
            "aesKey": "824531e8cad2a287",
            "account": "api@fsg.com.cn"
        }
    )



