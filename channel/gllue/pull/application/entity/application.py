import asyncio
from typing import Literal

from loguru import logger

from channel.gllue.pull.application.schema.application import GleSchema
from channel.gllue.pull.application.base.model import BaseResponseModel


class GleJsonEntity(GleSchema):
    # 每页最大条数
    total_count: int = 5

    def __init__(self, gle_user_config: dict):
        super().__init__(gle_user_config)
        self.b = []

    async def _get_candidate_info(self, entity: str,  page: int, field_name_list: str):
        res, status = await self.async_session.get(
            url=f"https://fsgtest.gllue.net/rest/{entity}/simple_list_with_ids",
            gle_config=self.gle_user_config.dict(),
            ssl=False,
            params={
                    "fields": field_name_list,
                    "ordering": "-lastUpdateDate",
                    "paginate_by": self.total_count,
                    'page': page},
            func=self.request_response_callback)
        logger.info(res)
        for candidate in res["result"][entity]:
            self.b.append(candidate)
        return res

    async def get_candidate_info(self, entity: str, page: int, field_name_list: str):

        candidate_list = await self._get_candidate_info(entity, page, field_name_list)
        logger.info(candidate_list)
        logger.info(f"获取到第{page}页")

    async def get_max_page(self, entity) -> int:
        field_name_list = await self.get_field_name_list(entity)
        field_name_list = ",".join(field_name_list)
        info = await self._get_candidate_info(entity=entity, page=1, field_name_list=field_name_list)
        i = BaseResponseModel(**info)
        logger.info("最大页数{}".format(i.totalpages))
        return i.totalpages

    async def run(self, entity: Literal["Candidate", "Position", "JobOrder"]):
        await self.check_token()
        max_page: int = await self.get_max_page(entity)
        field_name_list = await self.get_field_name_list(entity)
        field_name_list = ",".join(field_name_list)
        await asyncio.gather(
            *[
                self._get_candidate_info(entity=entity, page=_, field_name_list=field_name_list) for _ in range(1, max_page+1)
            ]
        )
        logger.error(self.b)
        return self.b

    async def check(self):
        i,x = await self.async_session.post(url=f"https://fsgtest.gllue.net/rest/file/simple_list_with_ids",ssl=False,
                                                    gle_config=self.gle_user_config.dict(),
                                                    func=self.request_response_callback)
        logger.info(i)


if __name__ == '__main__':
    asyncio.run(GleJsonEntity(
        {
            "apiServerHost": "https://fsgtest.gllue.net",
            "aesKey": "824531e8cad2a287",
            "account": "api@fsg.com.cn"
        }
    ).run("file"))