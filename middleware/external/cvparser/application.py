import aiohttp

from uuid import uuid4
from middleware.config import Settings
from middleware.exception import MiddlewareException
from middleware.external.cvparser.model import ParserRequest
from middleware.external.base.application import Application as BaseApplication


class Application(BaseApplication):
    @staticmethod
    async def parse_response_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            response = await res.text()
            raise MiddlewareException("解析失败, status: {}, response: {}".format(res.status, response))
        result = await res.json()
        return result

    async def parse(self, request_info: dict):
        request_info = ParserRequest(**request_info)
        form_data = aiohttp.FormData()
        form_data.add_field("file", request_info.fileContent, filename=request_info.fileName or "{}.pdf".format(
            uuid4().hex
        ))
        result = await self.settings.session.post(
            self.settings.resume_parser_url,
            data=form_data, func=self.parse_response_callback, ssl=False, timeout=300,
            params={"parse_avatar": "1" if request_info.parseAvatar else "false"}
        )
        return result


def get_app():
    return Application(Settings)
