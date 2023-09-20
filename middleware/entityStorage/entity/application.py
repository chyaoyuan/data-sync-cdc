from typing import Type

from utils.logger import logger

from middleware.entityStorage.base.application import BaseApplication
from middleware.entityStorage.entity.model import PutSourceModel, GetSourceModel
from middleware.settings.settings import Settings


class EntityApplication(BaseApplication):
    def __init__(self, settings: Type[Settings]):

        super().__init__(settings)

    async def put_entity(self, data: dict):
        data = PutSourceModel(**data)
        res, status = await self.session.put(
            f"{self.entity_storage_server_host}/v6/entity/{data.tenant}/{data.source_entity_type}/{data.source_id}",
             ssl=False,
             json=data.payload,
             func=self.request_response_callback)
        if status == 200:
            logger.info(f"Json原件存储成功 {data.tenant}={data.source_entity_type}={data.source_id}")
        else:
            logger.info(f"Json原件存储成失败 {data.tenant}={data.source_entity_type}={data.source_id}")

    async def get_entity(self, data: dict):

        data = GetSourceModel(**data)
        res, status = await self.session.get(
            f"{self.entity_storage_server_host}/v6/entity/{data.tenant}/{data.source_entity_type}/{data.source_id}",
            ssl=False,
            func=self.request_response_callback)
        if status == 404:
            logger.info(f"Json原件不存在 {data.tenant}={data.source_entity_type}={data.source_id}")
            return False, status
        elif status == 200:
            logger.info(f"Json原件获取成功 {data.tenant}={data.source_entity_type}={data.source_id}")
            return res, status
        else:
            logger.info(f"Json原件存储失败 {data.tenant}={data.source_entity_type}={data.source_id}")
            return res, status
