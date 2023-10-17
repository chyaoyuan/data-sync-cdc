import asyncio
import base64
import copy
import hashlib
import json
import os
import time
from asyncio import Task
from cgi import parse_header
from typing import Optional, Literal, List
from urllib.parse import unquote, urlencode

import aiofiles
import aiohttp


from channel.gllue.pull.application.attachment.application import GleAttachment
from channel.gllue.pull.application.base.application import BaseApplication
from channel.gllue.pull.application.entity.application import GleEntityApplication
from utils.logger import logger
from datetime import datetime

from channel.gllue.pull.application.model.sync_model import SyncConfig, BaseSyncConfig
from channel.gllue.pull.application.schema.application import GleSchema
from channel.gllue.pull.application.base.model import BaseResponseModel


class GleCandidateApplication(GleEntityApplication):
    add_field_list = []
    # add_field_list = ["attachments", "tags", "functions", "industrys", "locations"]
    entityType: str = "candidate".lower()
    # 每页最大条数
    total_count: int = 100
    # 每个请求延迟N秒
    sleep_time = 0
    # 最大并发数
    concurrency_level = 20

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

    async def init_schema(self):
        await self.schema_app.initialize_field_map_field(self.entityType)

    def create_extra_entity_id_map(self, result: dict):
        entity_type_list = list(result.keys())
        entity_type_list.remove(self.entityType)
        new_map = {}
        for entity_type in entity_type_list:
            new_map[entity_type] = self.schema_app._create_extra_entity_id_map(result)
        return new_map

    async def get_candidates_by_gql(self, gql: dict) -> List[Task]:
        """根据gql筛选，返回N个人才task"""
        gql_str = urlencode(gql)
        max_page: int = await self.get_max_page(gql_str)
        field_name_list = await self.schema_app.get_field_name_list(self.entityType)
        field_name_list = ",".join(field_name_list)
        task_list = [asyncio.create_task(
            self._get_entity_info(page=index, field_name_list=field_name_list, gql=gql_str)) for index in
            range(1, max_page + 1)]
        return task_list

    async def get_candidate_by_gql(self, gql: dict):
        """根据gql筛选，返回一个人才结果"""
        candidate_info_task_list = await self.get_candidates_by_gql(gql)
        for candidate_task in asyncio.as_completed(candidate_info_task_list):
            for candidate in await candidate_task:
                return candidate

    async def get_candidate_by_contact_gql(self, gql: dict) -> Optional[dict]:
        """
        分别用 手机号+邮箱/手机/邮箱在谷露系统搜索候选人,打中就返回
        """
        _gql = {k: v for k, v in gql.items() if v}
        # 先执行手机号+邮箱双重搜索，返回结果<=1
        candidate_info_task_list = await self.get_candidates_by_gql(_gql)
        for candidate_task in asyncio.as_completed(candidate_info_task_list):
            for candidate_list in await candidate_task:
                for candidate in candidate_list:
                    return candidate
        # 执行手机号搜索，返回结果<=1
        if _gql.get("mobile") or None:
            mobile = gql.get("mobile")
            candidate_info_task_list = await self.get_candidates_by_gql({"mobile": mobile})
            for candidate_task in asyncio.as_completed(candidate_info_task_list):
                for candidate_list in await candidate_task:
                    for candidate in candidate_list:
                        return candidate
        # # 执行邮箱搜索，返回结果<=1
        if _gql.get("email") or None:
            email = gql.get("email")
            candidate_info_task_list = await self.get_candidates_by_gql({"email": email})
            for candidate_task in asyncio.as_completed(candidate_info_task_list):
                for candidate_list in await candidate_task:
                    for candidate in candidate_list:
                        return candidate

    @staticmethod
    def pop_entity_file_content(entity_body: dict):
        """保存数据到TIP的时候要把附件的base64抹掉"""
        if attachments := entity_body.get("mesoorExtraAttachments", []):
            for attachment in attachments:
                attachment.pop("fileContent", None)
        entity_body.get("mesoorExtraLatestResume", {}).pop("fileContent", None)
        return entity_body



