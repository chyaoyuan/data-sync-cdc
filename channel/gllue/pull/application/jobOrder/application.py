import asyncio
from typing import Optional

from loguru import logger

from channel.gllue.pull.application.model.sync_model import SyncConfig
from channel.gllue.pull.application.schema.application import GleSchema
from channel.gllue.pull.application.base.model import BaseResponseModel
from urllib.parse import quote, parse_qsl

from utils.parse_time_interval import parse_time_interval
from urllib.parse import urlencode
from urllib.parse import parse_qs


class GleJobOrder(GleSchema):
    # 每页最大条数
    total_count: int = 100
    entity = "jobOrder".lower()
    # 前面是在entiy外的字段名称
    entity_map_config = {
        "entityFieldName": "client"
    }

    def __init__(self, gle_user_config: dict, sync_config: dict):
        super().__init__(gle_user_config)
        self.sync_config = SyncConfig(**sync_config)

        for field in ['lastContactDate__lastContactDate__day_range', 'lastUpdateDate__lastUpdateDate__day_range']:
            if field in self.sync_config.gql:
                raise Exception("GQL不允许配置时间参数 最后联系时间 及 最后更新时间 请在 recent和unit内指定")

        start_time, end_time = parse_time_interval({"unit": self.sync_config.unit, "recent": self.sync_config.recent})

        gql = {
            **dict(parse_qsl(self.sync_config.gql)),
            self.sync_config.timeFieldName: f"{start_time},{end_time}"
        }
        # https://www.cgladvisory.com/rest/joborder/list/facet?gql=jobStatus__s=Live&demandFacets=["client"]
        self.execute_gql = urlencode(gql)
        self.extra_fields_list: Optional[list] = self.sync_config.fieldNameList.split(",") if self.sync_config.fieldNameList else None

    async def get_job_info(self, page: int, field_name_list: str, check: bool = False, overwrite_sql: Optional[str] = None):
        async with self.semaphore:
            res, status = await self.async_session.get(
                url=f"{self.gle_user_config.apiServerHost}/rest/{self.entity}/simple_list_with_ids",
                ssl=False,
                params={"fields": field_name_list,
                        "ordering": "-lastUpdateDate",
                        "paginate_by": self.total_count,
                        'page': page,
                        'gql': overwrite_sql if overwrite_sql else self.execute_gql},
                func=self.request_response_callback)
            logger.info(overwrite_sql)
            if check:
                return res
            # 生成额外实体映射数据
            entity_map = {}
            extra_entity = list(res["result"].keys())
            extra_entity.remove(self.entity)
            for entity_name in extra_entity:
                entity_map[entity_name] = {entity_info["id"]: entity_info for entity_info in res["result"][entity_name]}
            # 以 "mesoorExtra"+ field_name的方式补进job里
            for job in res["result"][self.entity]:
                if filed_name_list := set(extra_entity).intersection(set(job.keys())):
                    for field_name in filed_name_list:
                        # 有个数据为null
                        job["mesoorExtra" + field_name] = entity_map[field_name].get(job[field_name], None)
            return [job for job in res["result"][self.entity]]

    async def get_max_page(self, overwrite_sql: Optional[str] = None) -> int:
        field_name_list = await self.get_field_name_list(self.entity)
        field_name_list = ",".join(field_name_list)
        info = await self.get_job_info(page=1, field_name_list=field_name_list, check=True,overwrite_sql=overwrite_sql)
        i = BaseResponseModel(**info)
        logger.info(f"每页{self.total_count}个 共{i.totalpages}页码 共{i.totalcount}个实体")
        return i.totalpages

    # async def get_job_order_status(self, job_order_id:str):
    #     res, status = await self.async_session.get(
    #         url=f"https://www.cgladvisory.com/rest/{self.entity}/list/facet",
    #         params={
    #             "gql": f'joborder={job_order_id}&joborder__is_deleted=false&demandFacets=["jobsubmission_status_kanban"]'
    #         },
    #         ssl=False,
    #         func=self.request_response_callback
    #     )
    #     logger.info(res)
    async def get_job_orders_by_gql(self, gql: dict):
        await self.check_token()
        gql_str = urlencode(gql)
        max_page: int = await self.get_max_page(gql_str)
        field_name_list = await self.get_field_name_list(self.entity)
        field_name_list = ",".join(field_name_list)
        task_list = [asyncio.create_task(
            self.get_job_info(page=index, field_name_list=field_name_list, check=False, overwrite_sql=gql_str))
            for index in range(1, max_page + 1)]
        return task_list

    async def get_job_order_by_gql(self, gql: dict):
        job_order_task_list = await self.get_job_orders_by_gql(gql)
        for job_order_task in asyncio.as_completed(job_order_task_list):
            for job_order in await job_order_task:
                if job_order["jobTitle"] == gql["jobTitle__icontains"]:
                    total_job_order_id = job_order["id"]
                    total_job_order_name = job_order["jobTitle"]
                    logger.info(f"jobOrder Exist: client_id->{gql['client__s']} name->{total_job_order_name} job_order_id->{total_job_order_id}")
                    return job_order
        return None

    async def run(self):
        await self.check_token()
        max_page: int = await self.get_max_page()
        field_name_list = await self.get_field_name_list(self.entity)
        if self.extra_fields_list:
            pass
        field_name_list = list(set(field_name_list + (self.extra_fields_list if self.extra_fields_list else [])))
        print(field_name_list)
        field_name_list = ",".join(field_name_list)

        task_list = [asyncio.create_task(self.get_job_info(page=index, field_name_list=field_name_list)) for index in range(1, max_page+1)]
        return task_list



