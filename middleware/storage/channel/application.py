import aiohttp

from loguru import logger
from middleware.exception import MiddlewareException
from middleware.storage.channel.model import ChannelBody
from middleware.storage.base.application import Application as BaseApplication


class Application(BaseApplication):
    @staticmethod
    async def save_channel_response_callback(res: aiohttp.ClientResponse):
        result: dict = await res.json()
        return result, res.status

    async def save_channel(self, body: dict, auth: str):
        request_body = ChannelBody(**body)
        response, status = await self.settings.session.put(
            self.settings.save_channel_url,
            headers={
                "Authorization": auth
            },
            json=request_body.dict(),
            func=self.save_channel_response_callback,
            timeout=120, ssl=False
        )
        result = response["result"]
        if status != 200:
            raise MiddlewareException("存储channel出错, channel body: {} status code: {} 原因: {}".format(
                request_body.dict(), status, response.get("message") or "未知原因"
            ))
        logger.info("{} channel 成功, space: {}, id: {}".format(
            "更新" if result.get("status") == "U" else "存储",
            result.get("spaceId") or "未知", result.get("channelId") or "未知"
        ))
