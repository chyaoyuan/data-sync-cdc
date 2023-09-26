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
from utils.logger import logger
from datetime import datetime

from channel.gllue.pull.application.model.sync_model import SyncConfig
from channel.gllue.pull.application.schema.application import GleSchema
from channel.gllue.pull.application.base.model import BaseResponseModel


class GleEntity(GleSchema):

    add_field_list = ["attachments", "tags", "functions", "industrys", "locations"]
    add_child_field_list = ["candidateexperience", "candidatequalification", "candidatelanguage", "candidateproject",
                            "candidateeducation"]
    entityType: str = "candidate".lower()

    # 每页最大条数
    total_count: int = 100
    # 每个请求延迟N秒
    sleep_time = 0
    # 最大并发数
    concurrency_level = 20

    def __init__(self, gle_user_config: dict, sync_config: dict):
        super().__init__(gle_user_config)
        self.sync_config = SyncConfig(**sync_config)
        self.semaphore = asyncio.Semaphore(self.concurrency_level)
        self.schema_config = {}
        self.get_industry_tag_schema_config = {}
        self.candidate_function_map = {}
        self.schema_app = GleSchema(gle_user_config)

        self.gle_user_id: Optional[int] = None

    async def init_schema(self):
        await self.schema_app.initialize_field_map_field(self.entityType)

    def merge_fields(self, source_entity_list: list, child_field_name_list: list, result):
        entity_list = []
        for index, candidate in enumerate(source_entity_list):
            entity_id = candidate["id"]
            entity = {**candidate}
            for child_field_name in child_field_name_list:
                _ = self.get_field_name_list_child_from_res(entity_id, self.entityType, result.get(child_field_name))
                entity[child_field_name] = _
            entity_list.append(entity)
        return entity_list

    @staticmethod
    def _create_extra_entity_id_map(entity_list):
        """将同时同步过来的其它实体生成map"""
        return {_["id"]: _ for _ in entity_list}

    def create_extra_entity_id_map(self, result: dict):
        entity_type_list = list(result.keys())
        entity_type_list.remove(self.entityType)
        new_map = {}
        for entity_type in entity_type_list:
            new_map[entity_type] = self._create_extra_entity_id_map(result)
        return new_map

    @staticmethod
    def split_string(input_string, max_len):
        segments = input_string.split(',')
        result = []

        current_segment = ''
        for segment in segments:
            if len(current_segment) + len(segment) <= max_len:
                current_segment += (',' if current_segment else '') + segment
            else:
                result.append(current_segment)
                current_segment = segment

        if current_segment:
            result.append(current_segment)

        return result

    async def ___get_candidate_info(self, page: int,
                                    field_name_list: str,
                                    check: bool = False,
                                    overwrite_gql: Optional[str] = None) -> dict:
        gql = overwrite_gql if overwrite_gql else self.sync_config.gql

        res, status = await self.async_session.get(
            url=self.settings.get_entity_url.format(entityType=self.entityType),
            ssl=False,
            params={
                "fields": field_name_list,
                "ordering": self.sync_config.orderBy,
                "paginate_by": self.total_count,
                'page': page,
                'gql': gql},
            func=self.request_response_callback)
        self.gle_user_id = res["@odata.user_id"]
        if check:
            return res
        if not res.get("result"):
            logger.warning(f"查询无结果->{self.entityType}->{gql}")
            return {}
        return res

    @staticmethod
    def pop_candidate_attachment_body(entity: dict):
        """附件的body从dict中去掉"""
        for attachment in entity.get("attachment", []):
            attachment.pop("fileContent", None)

    async def get_attachment(self, entity, attachments):
        attachments_info, status = await self.async_session.get(
            url=self.settings.get_entity_url.format(entityType="file"),
            ssl=False,
            params={
                "fields": "attachment",
                "gql": f"id__s={attachments}"},
            func=self.request_response_callback)
        entity["mesoorExtraAttachments"] = attachments_info['result']["attachment"]
        for attachment in entity["mesoorExtraAttachments"]:
            # {
            #      "dateAdded": "2023-09-20 22:11:43",
            #      "real_preview_path": "fsgtest/candidate/2023-09/preview/65ecc133-1f02-4872-bba6-37677e4e9890.pdf",
            #      "ext": "txt",
            #      "uuidname": "65ecc133-1f02-4872-bba6-37677e4e9890",
            #      "id": 824,
            #      "type": "candidate",
            #      "__name__": null,
            #      "__oss_url": "/rest/v2/attachment/preview/65ecc133-1f02-4872-bba6-37677e4e9890",
            #      "__download_oss_url": "/rest/v2/attachment/download/65ecc133-1f02-4872-bba6-37677e4e9890",
            #      "__preview_to_pdf": true
            # }
            con, headers = await self.async_session.get(
                url=attachment["__download_oss_url"],
                ssl=False,
                func=self.request_file_response_callback,
            )
            _, params = parse_header(headers.get("Content-Disposition"))
            filename = unquote(params.get('filename'))
            attachment["fileName"] = filename
            attachment["fileContent"] = base64.b64encode(con).decode()
        latest_date = None
        for attachment_info in entity["mesoorExtraAttachments"]:
            if attachment_info["type"] == "candidate":
                date_added = attachment_info["dateAdded"]
                if date_added is not None:
                    # 解析日期字符串为datetime对象
                    date_added = datetime.strptime(date_added, "%Y-%m-%d %H:%M:%S")
                    if latest_date is None or date_added > latest_date:
                        latest_date = date_added
                        latest_dict = attachment_info
                        entity["mesoorExtraLatestResume"] = latest_dict

    async def _get_candidate_info(self, page: int, field_name_list: str, check: bool = False,
                                  overwrite_gql: Optional[str] = None):
        async with self.semaphore:
            if self.sleep_time:
                await asyncio.sleep(self.sleep_time)
            response = await self.___get_candidate_info(page, field_name_list, check, overwrite_gql)
            # 当无权限人员拉数据会返回{}
            gql = overwrite_gql if overwrite_gql else self.sync_config.gql
            ids = gql.replace("id__s=", "").split(",")
            if not response:
                return [{"id": _id for _id in ids}], {}
            result = response.get("result", {})
            # 将外部字段合并
            child_field_name_list = self.get_field_name_list_child_from_field_list(field_name_list.split(","))
            candidate_list = self.merge_fields(result[self.entityType], child_field_name_list, result)
            for candidate in candidate_list:
                attachments = candidate.get("attachments") or None
                if attachments and self.sync_config.syncAttachment:
                    await self.get_attachment(candidate, attachments)
            # 获取除了本身以外还有哪些实体
            extra_entity_list = list(
                set(list(result.keys())) - set(child_field_name_list) - {self.entityType}
            )
            # 对额外实体合并
            extra_entity_map = {}
            for extra_entity_name in extra_entity_list:
                extra_entity_map[extra_entity_name] = self._create_extra_entity_id_map(result.get(extra_entity_name, []))
            # 对schema映射字典字段进行合并
            candidate_id_map = self.schema_app.field_id_map.get(self.entityType, {})
            # 对系统字段映射字典字段进行合并
            system_id_map = copy.deepcopy(self.schema_app.field_id_map)
            system_id_map.pop(self.entityType)
            for candidate in candidate_list:
                self.mesoor_extra(candidate, system_id_map, list(system_id_map.keys()))
                self.mesoor_extra(candidate, candidate_id_map, list(candidate_id_map.keys()))
                self.mesoor_extra(candidate, extra_entity_map, list(extra_entity_map.keys()))

            return candidate_list, response

    async def create_tasks(self, field_name_list):
        # 如果是指定抓取的ID列表
        if self.sync_config.syncModel == "Id":
            id_list = [self.sync_config.idList[i:i + self.total_count] for i in
                       range(0, len(self.sync_config.idList), self.total_count)]
            task_list = [
                self.get_candidate_info
                (1, field_name_list, overwrite_gql=f"id__s={','.join(_id_l)}")
                for _id_l in id_list]
        else:
            page_total = await self.get_max_page()
            task_list = [self.get_candidate_info(index_page, field_name_list) for index_page in
                         range(1, page_total + 1)]
        return task_list

    async def get_candidate_info(self, page: int, field_name_list: str, overwrite_gql: Optional[str] = None):
        candidate_list, source_response = await self._get_candidate_info(page, field_name_list, False, overwrite_gql)
        return candidate_list, source_response

    async def get_max_page(self, overwrite_gql: Optional[str] = None) -> int:
        info = await self.___get_candidate_info(page=1, field_name_list="id", check=True, overwrite_gql=overwrite_gql)
        i = BaseResponseModel(**info)
        return i.totalpages

    async def initialize_field(self, add_field_list: Optional[list] = None,
                               add_child_field_list: Optional[list] = None):
        # 生成字段map
        await self.schema_app.initialize_field_map_field(self.entityType)
        # 如果填写了子字段参数和额外子字段参数 则和默认值合并一起请求获取schema
        add_field_list = self.add_field_list if not add_field_list else add_field_list
        add_child_field_list = self.add_child_field_list if not add_child_field_list else add_child_field_list
        field_name_list = await self.get_field_name_list(self.entityType)
        self.schema_config[self.entityType] = set(list(field_name_list + add_field_list))
        for _ in set(add_child_field_list):
            field_name_list_child = await self.get_field_name_list_child(_)
            logger.info(f"添加额外子字段->{_}")
            self.schema_config[_] = field_name_list_child
            field_name_list = field_name_list + field_name_list_child
        field_name_list = field_name_list + add_field_list
        field_name_list = list(set(field_name_list))
        field_name_list = ",".join(field_name_list)
        return field_name_list

    async def get_candidates_by_gql(self, gql: dict) -> List[Task]:
        """根据gql筛选，返回N个人才task"""
        gql_str = urlencode(gql)
        max_page: int = await self.get_max_page(gql_str)
        field_name_list = await self.get_field_name_list(self.entityType)
        field_name_list = ",".join(field_name_list)
        task_list = [asyncio.create_task(
            self._get_candidate_info(page=index, field_name_list=field_name_list, overwrite_gql=gql_str)) for index in
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

        candidate_info_task_list = await self.get_candidates_by_gql(_gql)
        for candidate_task in asyncio.as_completed(candidate_info_task_list):
            for candidate in await candidate_task:
                return candidate
        if mobile := gql.get("mobile") or None:
            candidate_info_task_list = await self.get_candidates_by_gql({"mobile": mobile})
            for candidate_task in asyncio.as_completed(candidate_info_task_list):
                for candidate in await candidate_task:
                    return candidate
        if email := gql.get("email") or None:
            candidate_info_task_list = await self.get_candidates_by_gql({"email": email})
            for candidate_task in asyncio.as_completed(candidate_info_task_list):
                for candidate in await candidate_task:
                    return candidate

    @staticmethod
    def pop_entity_file_content(entity_body: dict):
        if attachments := entity_body.get("mesoorExtraAttachments", []):
            for attachment in attachments:
                attachment.pop("fileContent", None)
                print(9999)
        entity_body.get("mesoorExtraLatestResume", {}).pop("fileContent", None)
        return entity_body
