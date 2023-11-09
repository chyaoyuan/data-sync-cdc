import asyncio
import copy
import json
from typing import Optional
from urllib.parse import parse_qs, urlencode

import aiohttp

from channel.gllue.pull.application.attachment.application import GleAttachment
from channel.gllue.pull.application.base.application import BaseApplication
from channel.gllue.pull.application.entity.application import GleEntityApplication
from utils.logger import logger
from channel.gllue.pull.application.base.model import BaseResponseModel
from channel.gllue.pull.application.schema.application import GleSchema
from channel.gllue.pull.application.model.sync_model import SyncConfig, BaseSyncConfig
from utils.parse_time_interval import parse_time_interval
from urllib.parse import urlencode


class GlePullClient(GleEntityApplication):
    entityType = "client".lower()
    total_count: int = 5

    def __init__(self, gle_user_config: dict, base_sync_config: dict):
        super().__init__(gle_user_config, base_sync_config)
        self.base_sync_config = BaseSyncConfig(**base_sync_config)
        self.schema_config = {}
        self.candidate_function_map = {}
        # schema
        self.schema_app = GleSchema(gle_user_config)
        # 附件
        self.attachment_app = GleAttachment(gle_user_config)
        # 用户/操作者
        self.gle_user_id: Optional[int] = None



    # async def get_clients_by_gql(self, gql: dict):
    #     """
    #     通过GQL搜索公司
    #     """
    #     gql_str = urlencode(gql)
    #     max_page: int = await self.get_max_page(gql_str)
    #     field_name_list = await self.schema_app.get_field_name_list(self.entityType)
    #     field_name_list = ",".join(field_name_list)
    #     task_list = [asyncio.create_task(
    #         self.get_client_info(page=index, field_name_list=field_name_list, overwrite_gql=gql_str)) for index in
    #                  range(1, max_page + 1)]
    #     return task_list

    # async def get_client_by_gql(self, gql: dict):
    #     client_task_list = await self.get_clients_by_gql(gql)
    #     total_client_id = None
    #     for client_task in asyncio.as_completed(client_task_list):
    #         if total_client_id:
    #             break
    #         for client in await client_task:
    #             if client["name"] == gql["company_name__eq"]:
    #                 total_client_id = client["id"]
    #                 total_client_name = client["name"]
    #                 logger.info(f"client Exist name->{total_client_name} id->{total_client_id} info->{client}")
    #                 return client
    #     logger.info(f"client not Exist name->{gql['keyword']}")
    #     return None
