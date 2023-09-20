import asyncio
import json
from typing import Optional
from urllib.parse import parse_qs, urlencode

import aiohttp
from utils.logger import logger
from channel.gllue.pull.application.base.model import BaseResponseModel
from channel.gllue.pull.application.schema.application import GleSchema
from channel.gllue.pull.application.model.sync_model import SyncConfig
from utils.parse_time_interval import parse_time_interval
from urllib.parse import urlencode


class GlePullClient(GleSchema):
    # 每页最大条数

    total_count: int = 100
    entity = "client"

    def __init__(self, gle_user_config: dict, sync_config: dict):
        super().__init__(gle_user_config)
        # 同步需要的配置，搜索不需要
        self.sync_config = SyncConfig(**sync_config)
        self.semaphore = asyncio.Semaphore(48)

    async def get_client_info(self, page: int, field_name_list: str, check: bool = False, overwrite_gql: Optional[str]=False):
        async with self.semaphore:
            res, status = await self.async_session.get(
                url=self.settings.get_entity_url.format(entityType=self.entity),
                ssl=False,
                params={"fields": field_name_list,
                        "ordering": "-lastUpdateDate",
                        "paginate_by": self.total_count,
                        'page': page,
                        'gql': self.sync_config.gql if not overwrite_gql else overwrite_gql},
                func=self.request_response_callback)
            if check:
                return res
            return [entity for entity in res["result"][self.entity]]

    async def get_max_page(self, overwrite_gql: Optional[str] = None) -> int:
        field_name_list = await self.get_field_name_list(self.entity)
        field_name_list = ",".join(field_name_list)
        # field_name_list = "operation,id,is_parent,parent__id,parent__type,contractInfo,candidate_authorization_remind,type,name,__name__,citys,industrys,people_count,past_people_count,job_count,type,note_count,attachment_count,gllueext_bdsource"

        info = await self.get_client_info(page=1, field_name_list=field_name_list, check=True, overwrite_gql=overwrite_gql)
        i = BaseResponseModel(**info)
        logger.info(f"账户->{self.gle_user_config.account} 实体类型->{self.entity} 每页{self.total_count}个 共{i.totalpages}页码 共{i.totalcount}个实体")
        return i.totalpages

    async def run(self):
        max_page: int = await self.get_max_page()
        field_name_list = await self.get_field_name_list(self.entity)
        field_name_list = ",".join(field_name_list)
        # field_name_list = "operation,id,is_parent,parent__id,parent__type,contractInfo,candidate_authorization_remind,type,name,__name__,citys,industrys,people_count,past_people_count,job_count,type,note_count,attachment_count,gllueext_bdsource"
        task_list = [asyncio.create_task(self.get_client_info(page=index, field_name_list=field_name_list)) for index in
                     range(1, max_page + 1)]
        return task_list

    async def get_clients_by_gql(self, gql: dict):
        """
        通过GQL搜索公司
        """
        gql_str = urlencode(gql)
        max_page: int = await self.get_max_page(gql_str)
        field_name_list = await self.get_field_name_list(self.entity)
        field_name_list = ",".join(field_name_list)
        task_list = [asyncio.create_task(
            self.get_client_info(page=index, field_name_list=field_name_list, overwrite_gql=gql_str)) for index in
                     range(1, max_page + 1)]
        return task_list

    async def get_client_by_gql(self, gql: dict):
        client_task_list = await self.get_clients_by_gql(gql)
        total_client_id = None
        for client_task in asyncio.as_completed(client_task_list):
            if total_client_id:
                break
            for client in await client_task:
                if client["name"] == gql["company_name__eq"]:
                    total_client_id = client["id"]
                    total_client_name = client["name"]
                    logger.info(f"client Exist name->{total_client_name} id->{total_client_id} info->{client}")
                    return client
        logger.info(f"client not Exist name->{gql['keyword']}")
        return None




    # async def public_normal_company(self, company_id):
    #     form_data = aiohttp.FormData()
    #     form_data.add_field('data', json.dumps({"type": 'normal', "id": company_id}))
    #     res, status = await self.async_session.post(f"{self.gle_user_config.apiServerHost}/rest/client/add",
    #                                                 data=form_data,
    #                                                 gle_config=self.gle_user_config.dict(),
    #                                                 ssl=False, func=self.request_response_callback)
    #     if res["status"]:
    #         logger.info(f"公司修改成功->{company_id}")
    #         return
    #     logger.info(f"公司修改失败->{company_id} {res}")
    #
    # async def public_company_tag(self, company_id, tag: str):
    #
    #     form_data = aiohttp.FormData()
    #     form_data.add_field('data', json.dumps({"specialties": tag, "id": company_id}))
    #
    #     res, status = await self.async_session.post(f"{self.gle_user_config.apiServerHost}/rest/client/add",
    #                                                 data=form_data,
    #                                                 gle_config=self.gle_user_config.dict(),
    #                                                 ssl=False, func=self.request_response_callback)
    #     if res["status"]:
    #         logger.info(f"公司修改成功->{company_id}")
    #         return
    #     logger.error(f"公司修改失败->{company_id} {res}")



