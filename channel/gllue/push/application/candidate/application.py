import json
import urllib
from typing import Optional
from urllib.parse import urlencode
from urllib import request, parse
import aiohttp
from loguru import logger
from aiohttp import FormData
from channel.gllue.push.application.base.application import BaseApplication


class GlePushCandidate(BaseApplication):
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

    async def put_candidate_under_job_order_by_info(self, job_order: str, phone: str, email: str, name: str, overwrite_entity: Optional[dict]={}):
        data = {"candidateexperience_set":[{"is_current": True, "gllueext_text_1580804429654": "","gllueext_achievements":"","client":{"name":"mesoor-test1"}}],"candidateproject_set":[],"candidateeducation_set":[],"candidatelanguage_set":[],"englishName":"","owner":2491,"gllueext_select_1532920743234":"","gllueext_channelURL":"","gllueext_Summary":"","gllueext_text_miaoshu":"", "extractAttachments":False,"locations":"88","industrys":"11","functions":"3","channel":"400000","_notice_data":[]}
        new_data = {**data, **overwrite_entity, "joborder": job_order, "type":"candidate","mobile":phone,"chineseName":name,"email":email}
        body = "data=" + parse.quote(json.dumps(new_data, ensure_ascii=False))
        info, status = await self.async_session.post(
            url=f"{self.gle_user_config.apiServerHost}/rest/candidate/add",
            ssl=False,
            data=body,
            func=self.request_response_callback)
        logger.info(info)
        if status:
            return info["data"]

    async def push_candidate(self, entity: dict):
        info, status = await self.async_session.post(
            url=f"{self.gle_user_config.apiServerHost}/rest/candidate/add",
            ssl=False,
            json=entity,
            func=self.request_response_callback)
        if info["status"]:
            logger.info(f"候选人写回成功 id->{entity['id']}")
            return info
        else:
            logger.info(f"写回失败 id->{entity['id']} {info}")
