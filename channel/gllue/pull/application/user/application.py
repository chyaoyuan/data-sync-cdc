import asyncio
import base64
from cgi import parse_header
from copy import deepcopy
from typing import Optional, Literal, List
from urllib.parse import unquote, urlencode
from utils.logger import logger
from pydantic import BaseModel, Field
from datetime import datetime
from urllib.parse import quote
from collections import defaultdict
from channel.gllue.pull.application.model.sync_model import SyncConfig
from channel.gllue.pull.application.schema.application import GleSchema
from channel.gllue.pull.application.base.model import BaseResponseModel


class GleUser(GleSchema):
    # 每页最大条数
    total_count: int = 100
    entity: str = "user".lower()

    def __init__(self, gle_user_config: dict, sync_config: dict):
        super().__init__(gle_user_config)
        self.sync_config = SyncConfig(**sync_config)

    async def _get_entity_info(self, page: int, field_name_list: str, check: bool = False, overwrite_gql: Optional[str] = None):
        url = self.settings.get_entity_url.format(entityType=self.entity, apiServerHost=self.gle_user_config.apiServerHost)
        # 如果需求字段拼入url有超过url最大长度的危险则分开请求再组合
        res, status = await self.async_session.get(
            url=url,
            ssl=False,
            params={
                "fields": field_name_list,
                "ordering": "-lastUpdateDate",
                "paginate_by": self.total_count,
                'page': page,
                'gql': overwrite_gql if overwrite_gql else self.sync_config.gql
                    },
            func=self.request_response_callback)
        if check:
            return res
        # 获得不在json内的字段名
        return [i for i in res["result"][self.entity]]

    async def get_entity_info(self, page: int, field_name_list: str):
        entity_list = await self._get_entity_info(page, field_name_list, check=False)
        return entity_list

    async def get_max_page(self, overwrite_gql: Optional[str] = None) -> int:

        field_name_list = ["id"]
        field_name_list = ",".join(field_name_list)
        info = await self._get_entity_info(page=1, field_name_list=field_name_list, check=True,overwrite_gql=overwrite_gql)
        i = BaseResponseModel(**info)
        return i.totalpages

    async def initialize_field(self, add_field_list: Optional[list] = None, add_child_field_list: Optional[list] = None):
        # 如果填写了子字段参数和额外子字段参数 则和默认值合并一起请求获取schema
        add_field_list = [] if not add_field_list else add_field_list
        add_child_field_list = [] if not add_child_field_list else add_child_field_list
        field_name_list = await self.get_field_name_list(self.entity)
        for _ in set(add_child_field_list):
            field_name_list_child = await self.get_field_name_list_child(_)
            logger.info(f"添加额外子字段->{_} ->{field_name_list_child}")
            logger.info(field_name_list_child)
            field_name_list = field_name_list + field_name_list_child
        field_name_list = field_name_list + add_field_list
        field_name_list = list(set(field_name_list))
        field_name_list = ",".join(field_name_list)
        return field_name_list

    async def get_entity_by_gql(self, gql: dict):
        """
        通过GQL搜索公司
        """
        gql_str = urlencode(gql)
        max_page: int = await self.get_max_page(gql_str)
        field_name_list = await self.get_field_name_list(self.entity)
        field_name_list = ",".join(field_name_list)
        task_list = [asyncio.create_task(
            self._get_entity_info(page=index, field_name_list=field_name_list, overwrite_gql=gql_str)) for index in
                     range(1, max_page + 1)]
        return task_list

    async def get_user_by_gql(self, gql: dict):
        entity_info_task_list = await self.get_entity_by_gql(gql)
        for entity_task in asyncio.as_completed(entity_info_task_list):
            for entity in await entity_task:
                return entity











