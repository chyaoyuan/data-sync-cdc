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

from channel.gllue.pull.application.attachment.application import GleAttachment
from channel.gllue.pull.application.base.application import BaseApplication
from utils.logger import logger
from datetime import datetime

from channel.gllue.pull.application.model.sync_model import SyncConfig, BaseSyncConfig
from channel.gllue.pull.application.schema.application import GleSchema
from channel.gllue.pull.application.base.model import BaseResponseModel


class GleEntityApplication(BaseApplication):
    add_field_list = None
    entityType: str = None
    # 100jobsubmission会超长
    total_count: int = 100

    def __init__(self, gle_user_config: dict, base_sync_config: dict):
        super().__init__(gle_user_config)
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

    async def _get_entity_info(self, page: int, field_name_list: str, check: bool = False, gql: Optional[str] = None) -> dict:

        res, status = await self.async_session.get(
            url=self.settings.get_entity_url.format(entityType=self.entityType),
            func=self.request_response_callback,
            params=self.pop_useless_params({
                "fields": field_name_list,
                "ordering": self.base_sync_config.orderBy,
                "paginate_by": self.total_count,
                'page': page,
                'gql': gql})
        )

        self.gle_user_id = res["@odata.user_id"]
        if check:
            return res
        if not res.get("result"):
            logger.warning(f"无结果->{self.entityType}->{gql}")
            return {}
        return res

    @staticmethod
    def pop_candidate_attachment_body(entity: dict):
        """附件的body从dict中去掉"""
        for attachment in entity.get("attachment", []):
            attachment.pop("fileContent", None)

    async def get_entity_info(self, limit, page: int, sync_attachment: bool, field_name_list: str, gql: str, check: bool = False):
        # async with limit:
        response = await self._get_entity_info(page, field_name_list, check, gql)
        if not response:
            return [], {}
        result = response.get("result", {})
        # 将外部字段合并
        child_field_name_list = self.schema_app.get_field_name_list_child_from_field_list(field_name_list.split(","))
        entity_list = self.schema_app.merge_fields(self.entityType, result[self.entityType], child_field_name_list,result)

        for entity in entity_list:
            attachments = entity.get("attachments") or None
            if attachments and sync_attachment:
                attachments_ids = await self.attachment_app.get_attachment(attachments, entity)
                logger.info(f"get_attachment_success: type->{self.entityType} {entity['id']} attachments_ids->{attachments_ids}")
        # 获取除了本身以外还有哪些实体
        extra_entity_list = list(
            set(list(result.keys())) - set(child_field_name_list) - {self.entityType}
        )
        # 对额外实体合并
        extra_entity_map = {}
        for extra_entity_name in extra_entity_list:
            extra_entity_map[extra_entity_name] = self.schema_app._create_extra_entity_id_map(
                result.get(extra_entity_name, []))
        # 对schema映射字典字段进行合并
        entity_id_map = self.schema_app.field_id_map.get(self.entityType, {})
        # 对系统字段映射字典字段进行合并
        system_id_map = copy.deepcopy(self.schema_app.field_id_map)
        system_id_map.pop(self.entityType, None)
        for entity in entity_list:
            self.schema_app.mesoor_extra(entity, system_id_map, list(system_id_map.keys()))
            self.schema_app.mesoor_extra(entity, entity_id_map, list(entity_id_map.keys()))
            self.schema_app.mesoor_extra(entity, extra_entity_map, list(extra_entity_map.keys()))
        un_repeat_set = set()
        # 有的配置会导致生成两个相同实体，第一个信息全第二个不全，这里把它去重
        new_entity_list = []
        for entity in entity_list:
            _id = entity["id"]
            if _id not in un_repeat_set:
                new_entity_list.append(entity)
                un_repeat_set.add(_id)
        return new_entity_list, response

    async def create_tasks(self, field_name_list, sync_attachment: bool, id_list: Optional[List[int]] = None, gql: Optional[str] = None):
        _limit = asyncio.Semaphore(1)
        if self.base_sync_config.syncModel == "IdList" or self.base_sync_config.syncModel == "IdRecent":
            assert id_list
            if isinstance(id_list[0], int):
                id_list = [str(i) for i in id_list]
            _id_list = [id_list[i:i + self.total_count] for i in range(0, len(id_list), self.total_count)]
            task_list = [
                    self.get_entity_info
                    (_limit, 1, sync_attachment, field_name_list, gql=f"id__s={','.join(_id_l)}")
                        for _id_l in _id_list]
        else:
            page_total = await self.get_max_page(gql)
            task_list = [
                self.get_entity_info(_limit, index_page,sync_attachment, field_name_list, gql) for index_page in range(1, page_total + 1)]
        return task_list



    async def get_max_page(self, gql: Optional[str] = None) -> int:
        info = await self._get_entity_info(page=1, field_name_list="id", check=True, gql=gql)
        i = BaseResponseModel(**info)
        logger.info(f"实体{self.entityType}->有{i.totalpages}页 每页->{self.total_count} 总数为->{i.totalcount} gql->{gql}")
        return i.totalpages

    async def initialize_field(self, sync_attachment: bool,  extra_entity_name_list: Optional[List[str]] = None):

        schema = await self.schema_app.get_schema(self.entityType)
        logger.info(f"GleSchema entityType->{self.entityType} schema->{schema}")
        extra_entity_name_list = extra_entity_name_list if extra_entity_name_list else []
        await self.schema_app.initialize_field_map_field(self.entityType)
        entity_field_tree, _ = await self.schema_app.get_model_map_group()
        # extra_list = []
        # for entity_name in entity_field_tree.keys():
        #     fields_info_list: list = await self.schema_app.get_schema(entity_name)
        #     for fields_info in fields_info_list:
        #         if fields_info["name"] == self.entityType:
        #             extra_list.append(entity_name)
        # logger.info(extra_list)

        add_child_field_list = list(entity_field_tree.get(self.entityType, []))
        if add_child_field_list:
            logger.info(f"添加额外实体下实体->{add_child_field_list}")
        if self.entityType in add_child_field_list:
            add_child_field_list.remove(self.entityType)
        add_child_field_set = set(add_child_field_list + extra_entity_name_list)
        # 这个是获得主实体下所有字段的名字
        field_name_list = await self.schema_app.get_field_name_list(self.entityType)
        if sync_attachment:
            field_name_list.append("attachments")
        field_name_list_child = await self.schema_app.get_foreignkey(self.entityType)

        field_name_list = field_name_list_child + field_name_list
        self.schema_config[self.entityType] = set(list(field_name_list))
        for child_field in add_child_field_set:
            field_name_list_child = await self.schema_app.get_field_name_list_child(child_field)
            logger.info(f"添加额外子字段->{child_field}")
            self.schema_config[child_field] = field_name_list_child
            field_name_list = field_name_list + field_name_list_child
        field_name_list = list(set(field_name_list+["note"]))
        field_name_list = ",".join(field_name_list)

        return field_name_list

    async def initialize_field_test(self, extra_entity_name_list: Optional[List[str]] = None):
        await self.schema_app.get_foreignkey(self.entityType)

    def pop_entity_file_content(self, entity_body: dict):
        """保存数据到TIP的时候要把附件的base64抹掉"""
        entity_cache = entity_body
        if isinstance(entity_cache, dict):
            if attachments := entity_cache.get("mesoorExtraAttachments", []):
                for attachment in attachments:
                    attachment.pop("fileContent", None)
        elif isinstance(entity_cache, list):
            for _entity_cache in entity_cache:
                self.pop_entity_file_content(_entity_cache)

        return entity_body

    def get_entity_file_content(self, entity_body: dict, file_info_list: Optional[list] = None):
        if not file_info_list:
            file_info_list = []
        """保存数据到TIP的时候要把附件的base64抹掉"""
        entity_cache = entity_body
        if isinstance(entity_cache, dict):
            if attachments := entity_cache.get("mesoorExtraAttachments", []):
                file_info_list = file_info_list + attachments
        elif isinstance(entity_cache, list):
            for _entity_cache in entity_cache:
                self.get_entity_file_content(_entity_cache, file_info_list)
        return file_info_list


