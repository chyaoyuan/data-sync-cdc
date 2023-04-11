import aiohttp

from typing import List
from middleware.config import Settings
from middleware.exception import MiddlewareException
from middleware.mdwConvert.convert.model import RequestInfo
from middleware.mdwConvert.base.application import Application as BaseApplication


class Application(BaseApplication):
    @staticmethod
    async def convert_response_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            response = await res.text()
            raise MiddlewareException("转换出错, status: {}, response: {}".format(res.status, response))
        result = await res.json()
        return result["data"]

    async def convert(self, request_info: dict) -> List[dict]:
        request_info = RequestInfo(**request_info)
        result = await self.settings.session.post(
            self.settings.convert_url,
            json=request_info.dict(), func=self.convert_response_callback,
            ssl=False, timeout=120
        )
        return result


def get_convert_app():
    return Application(Settings)
