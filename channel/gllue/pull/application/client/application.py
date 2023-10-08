import asyncio
import json
from typing import Optional
from urllib.parse import parse_qs, urlencode

import aiohttp

from channel.gllue.pull.application.attachment.application import GleAttachment
from channel.gllue.pull.application.base.application import BaseApplication
from utils.logger import logger
from channel.gllue.pull.application.base.model import BaseResponseModel
from channel.gllue.pull.application.schema.application import GleSchema
from channel.gllue.pull.application.model.sync_model import SyncConfig
from utils.parse_time_interval import parse_time_interval
from urllib.parse import urlencode


class GlePullClient(BaseApplication):
    # 每页最大条数

    total_count: int = 100
    entityType = "client".lower()

    def __init__(self, gle_user_config: dict,x):
        super().__init__(gle_user_config)
        # 同步需要的配置，搜索不需要
        self.sync_config = SyncConfig(**x)
        self.schema_app = GleSchema(gle_user_config)
        self.attachment_app = GleAttachment(gle_user_config)
        self.semaphore = asyncio.Semaphore(48)

    async def get_client_info(self, page: int, field_name_list: str, check: bool = False, overwrite_gql: Optional[str]=False):
        async with self.semaphore:
            res, status = await self.async_session.get(
                url=self.settings.get_entity_url.format(entityType=self.entityType),
                ssl=False,
                params={"fields": field_name_list,
                        "ordering": "-lastUpdateDate",
                        "paginate_by": self.total_count,
                        'page': page,
                        'gql': self.sync_config.gql if not overwrite_gql else overwrite_gql},
                func=self.request_response_callback)
            logger.info(res)
            if check:
                return res
            return [entity for entity in res["result"][self.entityType]]

    async def get_max_page(self, overwrite_gql: Optional[str] = None) -> int:
        field_name_list = await self.schema_app.get_field_name_list(self.entityType)
        field_name_list = ",".join(field_name_list)
        # field_name_list = "operation,id,is_parent,parent__id,parent__type,contractInfo,candidate_authorization_remind,type,name,__name__,citys,industrys,people_count,past_people_count,job_count,type,note_count,attachment_count,gllueext_bdsource"

        info = await self.get_client_info(page=1, field_name_list=field_name_list, check=True, overwrite_gql=overwrite_gql)
        i = BaseResponseModel(**info)
        logger.info(f"账户->{self.gle_user_config.account} 实体类型->{self.entityType} 每页{self.total_count}个 共{i.totalpages}页码 共{i.totalcount}个实体")
        return i.totalpages

    async def run(self):
        max_page: int = await self.get_max_page()
        field_name_list = await self.schema_app.get_field_name_list(self.entityType)
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
        field_name_list = await self.schema_app.get_field_name_list(self.entityType)
        field_name_list = ",".join(field_name_list)
        task_list = [asyncio.create_task(
            self.get_client_info(page=index, field_name_list=field_name_list, overwrite_gql=gql_str)) for index in
                     range(1, max_page + 1)]
        return task_list

    async def create_tasks(self, field_name_list):
        if self.sync_config.syncModel == "Id":
            id_list = [self.sync_config.idList[i:i + self.total_count] for i in
                       range(0, len(self.sync_config.idList), self.total_count)]
            task_list = [
                self.get_client_info
                (1, field_name_list, overwrite_gql=f"id__s={','.join(_id_l)}")
                for _id_l in id_list]
        else:
            page_total = await self.get_max_page()
            task_list = [self.get_client_info(index_page, field_name_list) for index_page in
                         range(1, page_total + 1)]
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

if __name__ == '__main__':
    _gle_user_config = {
        "apiServerHost": "https://www.cgladvisory.com",
        "aesKey": "398b5ec714c59be2",
        "account": "system@wearecgl.com",
    }
    b = {
        "orderBy": "str",
        "syncModel": "str",
        # type__eq=prospect&
        'gql': "keyword=1106120"
    }

    async def exe():
        g = GlePullClient(_gle_user_config,b)
        entity_schema = await g.schema_app.get_field_name_list("client")
        entity_schema.append("attachments")
        print(entity_schema)
        task_list = await g.create_tasks(entity_schema)
        for candidate_task in asyncio.as_completed(task_list):
            entity_list = await candidate_task
            for entity in entity_list:
                logger.info(entity)

    asyncio.run(exe())