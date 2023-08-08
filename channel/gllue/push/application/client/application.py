import json
import aiohttp
from loguru import logger

from channel.gllue.push.application.base.application import BaseApplication


class GlePushClient(BaseApplication):

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
            logger.info(f"公司标签添加成功->{company_id}")
            return
        logger.error(f"公司标签添加失败->{company_id} {res}")

    async def check_client_exist(self, company_name: str):
        form_data = aiohttp.FormData()
        form_data.add_field('data', json.dumps({"name": company_name, "field_map": ["name","name1","name2","id","bd","type"]}))
        res, status = await self.async_session.post(f"{self.gle_user_config}/rest/client/check_sim_with_data",data=form_data,gle_config=self.gle_user_config.dict(), ssl=False, func=self.request_response_callback)
        if res and status == 200:
            if res["ststus"]:
                # 此公司存在
                return res
            else:
                # 此公司不存在
                return
        raise EOFError(f"{res} {status}")
