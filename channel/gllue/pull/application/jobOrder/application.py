import asyncio
from typing import Optional

from channel.gllue.pull.application.attachment.application import GleAttachment
from channel.gllue.pull.application.entity.application import GleEntityApplication
from utils.logger import logger

from channel.gllue.pull.application.model.sync_model import SyncConfig, BaseSyncConfig
from channel.gllue.pull.application.schema.application import GleSchema
from channel.gllue.pull.application.base.model import BaseResponseModel
from urllib.parse import quote, parse_qsl

from utils.parse_time_interval import parse_time_interval
from urllib.parse import urlencode
from urllib.parse import parse_qs


class GleJobOrder(GleEntityApplication):

    entityType: str = "jobOrder".lower()

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
    # async def get_job_orders_by_gql(self, gql: dict):
    #     gql_str = urlencode(gql)
    #     max_page: int = await self.get_max_page(gql_str)
    #     field_name_list = await self.get_field_name_list(self.entity)
    #     field_name_list = ",".join(field_name_list)
    #     task_list = [asyncio.create_task(
    #         self.get_job_info(page=index, field_name_list=field_name_list, check=False, overwrite_sql=gql_str))
    #         for index in range(1, max_page + 1)]
    #     return task_list
    #
    # async def get_job_order_by_gql(self, gql: dict):
    #     job_order_task_list = await self.get_job_orders_by_gql(gql)
    #     for job_order_task in asyncio.as_completed(job_order_task_list):
    #         for job_order in await job_order_task:
    #             if job_order["jobTitle"] == gql["jobTitle__eq"]:
    #                 total_job_order_id = job_order["id"]
    #                 total_job_order_name = job_order["jobTitle"]
    #                 logger.info(f"jobOrder Exist: client_id->{gql['client__s']} name->{total_job_order_name} job_order_id->{total_job_order_id}")
    #                 return job_order
    #     return None
    #
    # async def sync(self):
    #     max_page: int = await self.get_max_page()
    #     field_name_list = await self.get_field_name_list(self.entity)
    #     field_name_list = list(set(field_name_list + (self.extra_fields_list if self.extra_fields_list else [])))
    #     field_name_list = ",".join(field_name_list)
    #     task_list = [asyncio.create_task(self.get_job_info(page=index, field_name_list=field_name_list)) for index in range(1, max_page+1)]
    #     return task_list



