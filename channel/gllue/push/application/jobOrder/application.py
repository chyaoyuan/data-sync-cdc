import json
import aiohttp
from loguru import logger
from datetime import datetime
import pytz
from channel.gllue.push.application.base.application import BaseApplication


class GlePushJobOrder(BaseApplication):

    async def put_job_order(self, job_title: str, client_id: str, overwrite_info: dict):
        formatted_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
        form_data = aiohttp.FormData()
        default_info = {"positionType": "social", "totalCount": 1, "jobordercontact_set": [{"clientContact":2546031,"type":""}],"workflow_spec":"1","priority":"","openDate":"2023-08-28 13:17:54","jobStatus":"Live","gllueextBDcreditrate":"n88192761575119710","gllueextFeerate":"25","gllueextMinimumFee":"10","is_private":False,"joborderuser_set":[{"user":2491,"type":"Main Consultant"}],"shares":None,"citys":"102","annualSalary":10000,"maxAnnualSalary":20000,"gllueextcharge":"12","function":"1","gllueext_ttcjobopening":"ixYaEUQQ-Gs_Ga8S1x","description":"描述","gllueext_select_1640167799635":"kL44LRr1fN6kmCYckVcMR"}
        info = {**default_info, **overwrite_info, "jobTitle": job_title, "client": client_id}

        form_data.add_field("data", json.dumps(info))
        res, status = await self.async_session.post(f"{self.gle_user_config.apiServerHost}/rest/joborder/add",
                                                    data=form_data, ssl=False, func=self.request_response_callback)
        logger.info(res)
        if res and status == 200:
            if res["status"]:
                return {"id": res["data"]}
            else:
                return {"id": res["data"]}
        raise EOFError(f"{res} {status}")

    async def put_candidate_under_job_order_by_candidate_id(self, job_order_id: str, candidate_list: [str]):
        form_data = aiohttp.FormData()
        form_data.add_field("data", {"joborder_id": [job_order_id], "candidate_ids": candidate_list})
        # {"joborder_ids": [146974], "candidate_ids": [2545459], "startflow": "longlist", "origin_jobsubmission_id": 0}
        # response
        # {"status":true,"data":[{"status":true,"data":3414726,"current_message":{}}]}
        info, status = await self.async_session.post(
            url=f"{self.gle_user_config.apiServerHost}/rest/candidate/add",
            ssl=False,
            data=form_data,
            func=self.request_response_callback)
        logger.info(info)
        return info

