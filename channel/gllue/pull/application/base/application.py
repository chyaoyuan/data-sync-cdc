import asyncio

import aiohttp
from loguru import logger

from channel.gllue.pull.application.base.model import GleURL, GleUserConfig
from channel.gllue.session.gllue_aiohttp_session import GlHoMuraSession


class GleUrlConfig:
    get_entity_url = "{apiServerHost}/rest/{entityType}/simple_list_with_ids"
    get_entity_schema_url = "{apiServerHost}/rest/custom_field/{entityType}"

class BaseApplication:
    def __init__(self, gle_user_config: dict):
        self.async_session: GlHoMuraSession = GlHoMuraSession(
            aiohttp.ClientSession, retry_when=lambda x: not isinstance(x, asyncio.exceptions.TimeoutError)
        )
        self.settings = GleUrlConfig
        self.gle_user_config: GleUserConfig = GleUserConfig(**gle_user_config)
        self.gle_url = GleURL(GleUserConfig(**gle_user_config).apiServerHost)

    @staticmethod
    async def request_response_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            return await res.text(), res.status
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

    async def check_token(self):
        res, status = await self.async_session.get(self.gle_url.check,
                                                    params={"fields": "__name__%2Ccitys%2CjobTitle%2CtotalCount%2CjobStatus%2CopenDate%2Cbu____name__%2ClineManager__user%2Cjoborderuser_set__user____name__%2CaddedBy__user%2CdateAdded"},
                                                    ssl=False,
                                                    gle_config=self.gle_user_config.dict(),
                                                    func=self.request_response_callback)



if __name__ == '__main__':
    asyncio.run(BaseApplication(
        {
            "apiServerHost": "https://fsgtest.gllue.net",
            "aesKey": "824531e8cad2a287",
            "account": "api@fsg.com.cn"
        }
    ).check_token())


