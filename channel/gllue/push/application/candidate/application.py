import json
import urllib
from typing import Optional
from urllib.parse import urlencode
from urllib import request, parse
import aiohttp
from utils.logger import logger
from aiohttp import FormData
from channel.gllue.push.application.base.application import BaseApplication


class GlePushCandidate(BaseApplication):
    entity = "candidate"
    # 这么好用的接口GLLUE不给开放
    # async def check_candidate_exist(self, phone: Optional[str] = None, email: Optional[str] = None):
    #     for _ in [{"name": "mobile", "type": "mobile", "value": phone}, {"name": "email", "type": "email", "value": email}]:
    #         if _["value"]:
    #             form_data = FormData()
    #             form_data.add_field("data", _)
    #             info, status = await self.async_session.post(
    #                 url=f"{self.gle_user_config.apiServerHost}/rest/candidate/check",
    #                 data=form_data,
    #                 ssl=False,
    #                 func=self.request_response_callback
    #             )
    #             logger.info(info)
    #             if info["status"]:
    #                 return info["data"]
    #
    #     return False

    async def put_candidate_under_job_order_by_info(self,  required_entity: dict, overwrite_entity: dict):
        assert "job_order" in required_entity.keys()
        new_data = {**overwrite_entity, **required_entity, **{"type": "candidate"}}
        body = "data=" + parse.quote(json.dumps(new_data, ensure_ascii=False))
        info, status = await self.async_session.post(
            url=f"/rest/candidate/add",
            data=body,
            func=self.request_response_callback)
        logger.info(info)
        if status:
            return info["data"]

    async def upsert_candidate(self, entity: dict):
        info, status = await self.async_session.post(
            url=f"/rest/{self.entity}/add",
            ssl=False,
            json=entity,
            func=self.request_response_callback)
        if message := info.get("message"):
            logger.error(f"candidate 写回失败 message->{message}")
            return None
        if info["status"]:
            logger.info(f"candidate 写回成功 id->{info}")
            return info
        else:
            logger.error(f"candidate 写回失败 id->{entity['id']} {info}")

    async def create_candidate(self, overwrite_entity: dict):
        """
        entity_required:gllue指定的字段，不允许复写
        """
        # 创建简历就不许传递ID
        assert "id" not in overwrite_entity.keys()
        return await self.upsert_candidate(overwrite_entity)

    async def update_candidate(self, required_entity: dict, overwrite_entity: dict):
        """
        entity_required:gllue指定的字段，不允许复写
        """
        # 创建简历就不许传递ID
        assert "id" in overwrite_entity.keys()
        return await self.upsert_candidate({**overwrite_entity, **required_entity})


