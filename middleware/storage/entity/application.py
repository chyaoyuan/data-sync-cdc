import aiohttp

from utils.logger import logger
from middleware.exception import MiddlewareException
from middleware.storage.entity.model import EntityCustomFieldsBody
from middleware.storage.base.application import Application as BaseApplication


class Application(BaseApplication):
    @staticmethod
    async def save_entity_custom_fields_response_callback(res: aiohttp.ClientResponse):
        result = await res.json()
        if res.status != 200:
            raise MiddlewareException("更新实体自定义字段失败, 原因: {}".format(
                result.get("message") or "未知原因"
            ))
        return result["result"]

    async def save_entity_custom_fields(self, body: dict, auth: str):
        body = EntityCustomFieldsBody(**body)
        result = await self.settings.session.put(
            self.settings.save_entity_custom_fields_url,
            json=body.dict(), func=self.save_entity_custom_fields_response_callback,
            ssl=False, timeout=60, headers={"Authorization": auth}
        )
        logger.info("存储实体自定义字段成功, 实体类型: {} 实体id: {}".format(result["entityType"], result["entityId"]))
