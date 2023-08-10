import asyncio
from typing import Optional

from loguru import logger

from channel.gllue.pull.application.schema.application import GleSchema
from channel.gllue.pull.application.base.model import BaseResponseModel


class GleJobSubMissionInfo(GleSchema):
    # 每页最大条数
    total_count: int = 5

    def __init__(self, gle_user_config: dict):
        super().__init__(gle_user_config)
        self.entity = "jobSubMission"

    async def _get_job_sub_mission_info(self, page: int, field_name_list: str, job_order: str, gql: Optional[str]=None):
        url = self.settings.get_entity_url.format(apiServerHost=self.gle_user_config.apiServerHost, entityType=self.entity)
        res, status = await self.async_session.get(
            url=url,
            ssl=False,
            params={"fields": field_name_list,
                    "ordering": "-lastUpdateDate",
                    "paginate_by": self.total_count,
                    'page': page,
                    "joborder": job_order,
                 },
            func=self.request_response_callback)
        if res.get("message") or None:
            raise Exception(f"{res}==={status}==={url}")

        return res

    # async def get_job_sub_mission_info(self, page: int, field_name_list: str):
    #
    #     candidate_list = await self._get_job_sub_mission_info(page, field_name_list)
    #     logger.info(candidate_list)
    #     logger.info(f"获取到第{page}页")

    async def get_max_page(self, job_order: str, gql: Optional[str] = None) -> int:
        field_name_list = await self.get_field_name_list(self.entity)
        field_name_list = ",".join(field_name_list)
        info = await self._get_job_sub_mission_info(page=1, field_name_list=field_name_list, job_order=job_order, gql=gql)
        i = BaseResponseModel(**info)
        logger.info("最大页数{}".format(i.totalpages))
        return i.totalpages

    # async def run(self):
    #     await self.check_token()
    #     max_page: int = await self.get_max_page()
    #     field_name_list = await self.get_field_name_list("jobsubmission".lower())
    #     field_name_list = ",".join(field_name_list)
    #     await asyncio.gather(
    #         *[
    #             self._get_job_sub_mission_info(page=_, field_name_list=field_name_list) for _ in range(1, max_page+1)
    #         ]
    #     )

    async def sync_job_submission_by_job_order_id(self, job_order_id: str, field_name_list: str):
        # 因为之前同步JobOrder已经测试过token了就不在这里测试了
        max_page: int = await self.get_max_page(job_order_id)
        task_list = [
            asyncio.create_task(
                self._get_job_sub_mission_info(page=_, field_name_list=field_name_list, job_order=job_order_id)
            ) for _ in range(1, max_page+1)
        ]
        return task_list



if __name__ == '__main__':
    asyncio.run(GleJobSubMissionInfo(
        {
            "apiServerHost": "https://www.cgladvisory.com",
            "aesKey": "eae48bfe137cc656",
            "account": "system@wearecgl.com"
        }
    ).run())