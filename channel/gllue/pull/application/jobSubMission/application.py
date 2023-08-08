import asyncio

from loguru import logger

from channel.gllue.pull.application.schema.application import GleSchema
from channel.gllue.pull.application.base.model import BaseResponseModel


class GleJobSubMissionInfo(GleSchema):
    # 每页最大条数
    total_count: int = 5

    def __init__(self, gle_user_config: dict):
        super().__init__(gle_user_config)
        self.entity = "jobSubMission"

    async def _get_job_sub_mission_info(self, page: int, field_name_list: str):
        url = self.settings.get_entity_url.format(apiServerHost=self.gle_user_config.apiServerHost, entityType=self.entity)
        res, status = await self.async_session.get(
            url=url,
            gle_config=self.gle_user_config.dict(),
            ssl=False,
            params={"fields": field_name_list,
                    "ordering": "-lastUpdateDate",
                    "paginate_by": self.total_count,
                    'page': page},
            func=self.request_response_callback)
        logger.info(res)

        return res

    async def get_job_sub_mission_info(self, page: int, field_name_list: str):

        candidate_list = await self._get_job_sub_mission_info(page, field_name_list)
        logger.info(candidate_list)
        logger.info(f"获取到第{page}页")

    async def get_max_page(self) -> int:
        field_name_list = await self.get_field_name_list("jobsubmission")
        field_name_list = ",".join(field_name_list)
        info = await self._get_job_sub_mission_info(page=1, field_name_list=field_name_list)
        logger.info(info)
        i = BaseResponseModel(**info)
        logger.info("最大页数{}".format(i.totalpages))
        return i.totalpages

    async def run(self):
        await self.check_token()
        max_page: int = await self.get_max_page()
        field_name_list = await self.get_field_name_list("jobsubmission")
        field_name_list = ",".join(field_name_list)
        await asyncio.gather(
            *[
                self._get_job_sub_mission_info(page=_, field_name_list=field_name_list) for _ in range(1, max_page+1)
            ]
        )


if __name__ == '__main__':
    asyncio.run(GleJobSubMissionInfo(
        {
            "apiServerHost": "https://www.cgladvisory.com",
            "aesKey": "eae48bfe137cc656",
            "account": "system@wearecgl.com"
        }
    ).run())