import json
import aiohttp
import urllib.parse as urlparse

from loguru import logger
from middleware.config import Settings
from middleware.exception import MiddlewareException
from middleware.external.base.application import Application as BaseApplication
from middleware.external.transmitter.model import SaveDataRequest, GetDataRequest, DeleteEntityRequest


class Application(BaseApplication):
    @staticmethod
    async def save_data_response_callback(res: aiohttp.ClientResponse):
        response = None
        if not 200 <= res.status <= 300:
            response = await res.text()
        return res.status, response

    @staticmethod
    async def get_data_response_callback(res: aiohttp.ClientResponse):
        response = await res.text()
        return res.status, response

    async def get_data(self, request_info: dict):
        request_info = GetDataRequest(**request_info)
        logger.info(
            self.settings.transmitter_v2_get_entity_url.format(
                tenant=request_info.tenant, entityType=request_info.entityType, entityId=request_info.entityId
            ))
        status, response = await self.settings.session.get(
            self.settings.transmitter_v2_get_entity_url.format(
                tenant=request_info.tenant, entityType=request_info.entityType, entityId=request_info.entityId
            ), func=self.get_data_response_callback, ssl=False, timeout=120
        )
        if status == 404:
            return
        elif status != 200:
            raise MiddlewareException("{} 获取实体 {} id {} 数据失败, status: {}, response: {}".format(
                request_info.tenant, request_info.entityType, request_info.entityId, status, response
            ))
        return json.loads(response)

    async def save_data(self, request_info: dict):
        request_info = SaveDataRequest(**request_info)
        entity_size = len(json.dumps(request_info.entity, ensure_ascii=False))
        if entity_size > self.settings.max_transmitter_entity_size:
            logger.error("{} 实体大小超过 {} bytes, 当前实体大小为: {} bytes, 不予存储".format(
                request_info.tenant, self.settings.max_transmitter_entity_size, entity_size)
            )
            return
        status, response = await self.settings.session.put(
            self.settings.transmitter_v2_save_entity_url.format(
                tenant=request_info.tenant, entityType=request_info.entityType, entityId=request_info.entityId
            ), func=self.save_data_response_callback, ssl=False,
            timeout=120, json=request_info.entity, headers={
                "X-Source": urlparse.quote_plus(request_info.source),
                "X-Editor": urlparse.quote_plus(request_info.editor or self.settings.transmitter_editor)
            }
        )
        if status != 200:
            raise MiddlewareException("{} 存储实体 {} {} 失败, status: {}, response: {}={}".format(
                request_info.tenant, request_info.entityType, request_info.entityId, status, response, request_info.entity
            ))
        logger.info("{} 存储实体 {} {} 成功".format(request_info.tenant, request_info.entityType, request_info.entityId))

    @staticmethod
    async def delete_entity_response_callback(res: aiohttp.ClientResponse):
        response = await res.text()
        return res.status, response

    async def delete_entity(self, request_info: dict):
        request_info = DeleteEntityRequest(**request_info)
        status, response = await self.settings.session.delete(
            self.settings.transmitter_v2_delete_entity_url.format(
                tenant=request_info.tenant, entityType=request_info.entityType, entityId=request_info.entityId
            ), ssl=False, timeout=120, func=self.delete_entity_response_callback,
            headers={
                "X-Editor": request_info.editor, "X-Source": request_info.source
            }
        )
        logger.info(status)
        if status not in [200, 404]:
            raise MiddlewareException("{} 删除实体 {} id {} 失败, response: {}, status: {}".format(
                request_info.tenant, request_info.entityType, request_info.entityId, response, status
            ))
        if status == 200:
            logger.info("{} 删除实体 {} id {} 成功".format(
                request_info.tenant, request_info.entityType, request_info.entityId
            ))
        elif status == 404:
            logger.info("{} 删除实体 {} id {} 实体不存在".format(
                request_info.tenant, request_info.entityType, request_info.entityId
            ))




def get_app():
    return Application(Settings)
