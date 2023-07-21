import json

import aiohttp
from loguru import logger

from channel.gllue.pull.application.schema.application import GleSchema


class GlePullClient(GleSchema):
    # 每页最大条数
    total_count: int = 5

    def __init__(self, gle_user_config: dict):
        super().__init__(gle_user_config)

    async def public_normal_company(self, company_id):
        form_data = aiohttp.FormData()
        form_data.add_field('data', json.dumps({"type": 'normal', "id": company_id}))
        res, status = await self.async_session.post(f"{self.gle_user_config.apiServerHost}/rest/client/add",
                                                    data=form_data,
                                                    gle_config=self.gle_user_config.dict(),
                                                    ssl=False, func=self.request_response_callback)
        if res["status"]:
            logger.info(f"公司修改成功->{company_id}")
            return
        logger.info(f"公司修改失败->{company_id} {res}")

    async def public_company_tag(self, company_id, tag: str):

        form_data = aiohttp.FormData()
        form_data.add_field('data', json.dumps({"specialties": tag, "id": company_id}))

        res, status = await self.async_session.post(f"{self.gle_user_config.apiServerHost}/rest/client/add",
                                                    data=form_data,
                                                    gle_config=self.gle_user_config.dict(),
                                                    ssl=False, func=self.request_response_callback)
        if res["status"]:
            logger.info(f"公司修改成功->{company_id}")
            return
        logger.error(f"公司修改失败->{company_id} {res}")



