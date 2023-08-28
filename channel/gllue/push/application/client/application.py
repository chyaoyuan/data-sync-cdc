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
                                                    ssl=False, func=self.request_response_callback)
        if res["status"]:
            logger.info(f"公司标签添加成功->{company_id}")
            return
        logger.error(f"公司标签添加失败->{company_id} {res}")

    async def check_client_exist(self, company_name: str):
        form_data = aiohttp.FormData()
        form_data.add_field('data', json.dumps({"name": company_name, "field_map": ["name","name1","name2","id","bd","type"]}))
        res, status = await self.async_session.post(f"{self.gle_user_config}/rest/client/check_sim_with_data",data=form_data,ssl=False, func=self.request_response_callback)
        if res and status == 200:
            if res["ststus"]:
                # 此公司存在
                return res
            else:
                # 此公司不存在
                return
        raise EOFError(f"{res} {status}")

    async def put_client(self, client_name: str, overwrite_info: dict):
        form_data = aiohttp.FormData()
        default_info = {"gllueext_bdsource": "", "is_parent": 2, "parent": None, "_notice_data": [], "type": "prospect"}
        info = {**default_info, **overwrite_info, "name": client_name}
        form_data.add_field("data", json.dumps(info))
        res, status = await self.async_session.post(f"{self.gle_user_config.apiServerHost}/rest/client/add",
                                                    data=form_data, ssl=False, func=self.request_response_callback)

        if res and status == 200:
            if res["status"]:
                # 此公司存在
                # {'status': True, 'data': 2127520, 'current_message': {}}
                logger.info(f"client Create success name->{info['name']} id->{res['data']}")
                return {"id": res["data"], "name": info["name"]}

            else:
                # 此公司不存在
                # {'status': False, 'message': 'Duplicate Info: Duplicate company! ID: 2127516', 'data': 2127516}
                raise Exception(f'{info["name"]} 已存在->{res}')
        raise EOFError(f"{res} {status}")

    async def put_job_order(self, info: dict):
        form_data = aiohttp.FormData()
        default_info = {"positionType":"social","priority":"","jobStatus":"Live","jobordercontact_set":[{"clientContact":2409672,"type":""}],"workflow_spec":"1","is_private":True,"joborderuser_set":[{"user":2491,"type":"Main Consultant"}],"totalCount":1,"gllueextFeerate":"25","gllueextMinimumFee":"10","openDate":"2023-08-22 16:25:21","gllueextBDcreditrate":"n88192761575119710","shares":None,"citys":"102","annualSalary":10000,"maxAnnualSalary":0,"client":1023759,"function":"311","gllueextcharge":"1","gllueext_ttcjobopening":"ixYaEUQQ-Gs_Ga8S1x","description":"描述","gllueext_select_1640167799635":"kL44LRr1fN6kmCYckVcMR"}
        info = {**default_info, **info}
        assert info.get("jobTitle") or None
        info = {"positionType":"social","priority":"","jobStatus":"Live","jobordercontact_set":[{"clientContact":2409672,"type":""}],"workflow_spec":"1","is_private":False,"joborderuser_set":[{"user":2491,"type":"Main Consultant"}],"totalCount":1,"gllueextFeerate":"25","gllueextMinimumFee":"10","openDate":"2023-08-22 16:25:21","gllueextBDcreditrate":"n88192761575119710","shares":[],"citys":"102","annualSalary":10000,"maxAnnualSalary":0,"client":1023759,"jobTitle":"测试项目","function":"311","gllueextcharge":"1","gllueext_ttcjobopening":"ixYaEUQQ-Gs_Ga8S1x","description":"描述","gllueext_select_1640167799635":"kL44LRr1fN6kmCYckVcMR"}
        form_data.add_field("data", json.dumps(info))
        res, status = await self.async_session.post(f"{self.gle_user_config.apiServerHost}/rest/joborder/add",
                                                    data=form_data, ssl=False, func=self.request_response_callback)
        print(res)
        print(status)
        if res and status == 200:
            if res["status"]:
                # 此公司存在
                # {'status': True, 'data': 2127520, 'current_message': {}}
                return res
            else:
                # 此公司不存在
                # {'status': False, 'message': 'Duplicate Info: Duplicate company! ID: 2127516', 'data': 2127516}
                return
        raise EOFError(f"{res} {status}")

    async def put_submission_candidate(self, info: dict):
        form_data = aiohttp.FormData()
        default_info = {"positionType":"social","priority":"","jobStatus":"Live","jobordercontact_set":[{"clientContact":2409672,"type":""}],"workflow_spec":"1","is_private":True,"joborderuser_set":[{"user":2491,"type":"Main Consultant"}],"totalCount":1,"gllueextFeerate":"25","gllueextMinimumFee":"10","openDate":"2023-08-22 16:25:21","gllueextBDcreditrate":"n88192761575119710","shares":None,"citys":"102","annualSalary":10000,"maxAnnualSalary":0,"client":1023759,"function":"311","gllueextcharge":"1","gllueext_ttcjobopening":"ixYaEUQQ-Gs_Ga8S1x","description":"描述","gllueext_select_1640167799635":"kL44LRr1fN6kmCYckVcMR"}
        info = {**default_info, **info}

        info = {"joborder": 146834,"type": "candidate","candidateexperience_set":[{"gllueext_text_1580804429654":"","gllueext_achievements":"","start":"1970-01","is_current":False,"client":{"name":"测试公司","id":None}}],"candidateproject_set":[],"candidateeducation_set":[],"candidatelanguage_set":[],"gllueext_select_1532920743234":"","gllueext_channelURL":"","chineseName":"测试","englishName":"","owner":2491,"gllueext_Summary":"","gllueext_text_miaoshu":"","mobile":"17612305718","locations":"144","extractAttachments":False,"email":"77704383@qqq.com","functions":"3","industrys":"13","channel":"100008","_notice_data":[]}
        form_data.add_field("data", json.dumps(info))
        res, status = await self.async_session.post(f"{self.gle_user_config.apiServerHost}/rest/candidate/add",
                                                    data=form_data, ssl=False, func=self.request_response_callback)
        print(res)
        print(status)
        if res and status == 200:
            if res["status"]:
                # 此公司存在
                # {'status': True, 'data': 2127520, 'current_message': {}}
                return res
            else:
                # 此公司不存在
                # {'status': False, 'message': 'Duplicate Info: Duplicate company! ID: 2127516', 'data': 2127516}
                return
        raise EOFError(f"{res} {status}")
