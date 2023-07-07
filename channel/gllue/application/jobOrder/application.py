import asyncio

from loguru import logger

from channel.gllue.application.schema.application import GleSchema
from channel.gllue.application.base.model import BaseResponseModel


class GleJobOrder(GleSchema):
    # 每页最大条数
    total_count: int = 5

    def __init__(self, gle_user_config: dict):
        super().__init__(gle_user_config)
        self.b = []

    async def _get_job_info(self, page: int, field_name_list: str):
        res, status = await self.async_session.get(
            url="https://fsgtest.gllue.net/rest/joborder/simple_list_with_ids",
            gle_config=self.gle_user_config.dict(),
            ssl=False,
            params={"fields": field_name_list,
                    "ordering": "-lastUpdateDate",
                    "paginate_by": self.total_count,
                    'page': page},
            func=self.request_response_callback)
        for job in res["result"]["joborder"]:
            logger.info(f"{job['id']}===={job}")

        return res

    async def get_job_info(self, page: int, field_name_list: str):

        job_list = await self._get_job_info(page, field_name_list)
        logger.info(job_list)
        logger.info(f"获取到第{page}页")

    async def get_max_page(self) -> int:
        field_name_list = await self.get_field_name_list("joborder")
        field_name_list = ",".join(field_name_list)
        info = await self._get_job_info(page=1, field_name_list=field_name_list)
        i = BaseResponseModel(**info)
        logger.info("最大页数{}".format(i.totalpages))
        return i.totalpages

    async def run(self):
        await self.check_token()
        max_page: int = await self.get_max_page()
        field_name_list = await self.get_field_name_list("Candidate")
        field_name_list.append("tags")
        field_name_list = ",".join(field_name_list)
        await asyncio.gather(
            *[
                self._get_job_info(page=_, field_name_list=field_name_list) for _ in range(1, max_page+1)
            ]
        )
        return self.b


if __name__ == '__main__':
    asyncio.run(GleJobOrder(
        {
            "apiServerHost": "https://fsgtest.gllue.net",
            "aesKey": "824531e8cad2a287",
            "account": "api@fsg.com.cn"
        }
    ).run())