import asyncio
import time

import jmespath
import requests
from loguru import logger

from channel.gllue.pull.application.applicaiton import GlePullApplication
from channel.gllue.executor.config import gllue_industry_config_map, gllue_zhienng_config_map
from channel.gllue.push.application.application import GlePushApplication
from middleware.application import mid
# 如果解析结果没有则使用原值的字段

# 如果只有此字段则不推送
_if_only_exist = ["id"]


def get_gle_func_id(func_name_list: list):
    res = []
    for industry in func_name_list:
        gllue_industry_id = gllue_zhienng_config_map.get(industry)
        if gllue_industry_id:
            res.append(str(gllue_industry_id))
    return ",".join(res)


def get_gle_industry_id(industry_name_list: list):
    res = []
    print(industry_name_list)
    for industry in industry_name_list:
        gllue_industry_id = gllue_industry_config_map.get(industry)
        if gllue_industry_id:
            res.append(str(gllue_industry_id))
    return ",".join(res)


def create_need_remove_key_list(if_exist_not_push_list: list, data: dict):
    need_remove_key_list = []
    for jmespath_grama in if_exist_not_push_list:
        verify = jmespath.search(jmespath_grama, data)
        if verify:
            need_remove_key_list.append(jmespath_grama)
    return need_remove_key_list


def remove_key(need_remove_key_list:list, data: dict):
    for key in need_remove_key_list:
        data.pop(key)


def only_key_check(_if_only_exist: list, data: dict):
    data_key_list = data.keys()
    for data_key in data_key_list:
        if data_key not in _if_only_exist:
            return False
    return True


async def sync_candidate_pull_and_push(gle_user_config: dict, sync_config: dict):
    candidate_pull_app = GlePullApplication(gle_user_config, sync_config).candidate_app
    candidate_push_app = GlePushApplication(gle_user_config).candidate_app

    await candidate_pull_app.check_token()
    field_name_list: str = await candidate_pull_app.initialize_field()
    page_total = await candidate_pull_app.get_max_page()

    for index_page in range(1, page_total + 1):
        entity_list = await candidate_pull_app.get_candidate_info(index_page, field_name_list)
        logger.info(f"第{index_page}页 entity->{candidate_pull_app.entity} id->{[entity['id'] for entity in entity_list]}")
        for entity in entity_list:
            gle_id = entity["id"]
            entity["locations"] = str(entity["locations"])

            # # 判断变动
            # old_entity, status = await mid.entity_storage_mid.entity_storage_app.get_entity({"tenant": "wf-test","source_entity_type":"candidate","source_id":gle_id})
            # if status == 200 and old_entity.get("latestResume") and entity.get("latestResume"):
            #     old_entity_last_resume = old_entity.get("latestResume")
            #     new_entity_last_resume = entity.get("latestResume")
            #     if old_entity_last_resume == new_entity_last_resume:
            #         logger.info(f"gle {gle_id}没有更新简历附件 跳过")
            #         continue

            if entity.get("latestResume") or None:
                latest_resume_info = entity.get("latestResume")
                headers = {
                    'Authorization': 'APPCODE ' + "085c11ede59c44588116918f0d3ee1ed",
                    'Content-Type': 'application/json; charset=UTF-8',
                }

                data = {
                    "file_name": latest_resume_info["fileName"],
                    "file_cont": latest_resume_info["fileContent"],
                    "need_avatar": 1,
                    "ocr_type": 1,
                    "need_social_exp": 1,
                }
                res = requests.post("http://resumesdk.market.alicloudapi.com/ResumeParser", json=data, headers=headers)
                if res.status_code == 200:
                    data = {"task_ids": ["Resumegl:standard:2023_07_03_09_34_35"], "data": [res.json()["result"]]}
                    convert_res = requests.post("http://converter.nadileaf.com/v2/converter", json=data)
                    if convert_res.status_code == 200:
                        gle_entity = convert_res.json()["data"][0]
                        gle_entity["id"] = gle_id
                        if gle_entity.keys() == ["id"]:
                            logger.info(f"{gle_id}无转换结果")
                            continue
                        # 职位名标签
                        job_title_list = list(set([_.get("title") for _ in gle_entity.get("candidateexperience_set",[]) if _.get("title",)]))
                        job_tag = await mid.tag_mid.tag_app.un_repeat_tag(job_title_list,"position3")
                        logger.info(f"职能为->{job_tag}")
                        if job_tag:
                            gle_entity["tags"] = job_tag
                            logger.info(f"职能为->{get_gle_func_id(job_tag)}")
                            gle_entity["functions"] = get_gle_func_id(job_tag)
                        company_name_list = list(set([_.get("client", {}).get("name") for _ in gle_entity.get("candidateexperience_set",[]) if _.get("client", {}).get("name")]))
                        industry_tag = await mid.tag_mid.tag_app.un_repeat_tag(company_name_list, "industry2")

                        # 曾就职公司名标签
                        # industry_tag = ["互联网/IT/电子/通信-电子商务"]
                        logger.info(f"行业为->{industry_tag}")
                        if industry_tag:
                            logger.info(f"行业为->{get_gle_industry_id(industry_tag)}")
                            gle_entity["industrys"] = get_gle_industry_id(industry_tag)
                        # 如果存在则抹除
                        _if_exist_not_push_list = ["expected_salary", "dateOfBirth", 'locations']
                        for _ in _if_exist_not_push_list:
                            if _ in entity.keys():
                                gle_entity.pop(_, None)

                        info = await candidate_push_app.push_candidate(gle_entity)

                        # get company id
                        # if info:
                        #     # 写回成功
                        #     await mid.entity_storage_mid.entity_storage_app.put_entity(
                        #         {"tenant": "wf-test", "source_entity_type": "candidate", "source_id": gle_id,
                        #          "payload": entity})
                        #     experience_list = info.get("current_message", {}).get("candidateexperience", [])
                        #     for experience in experience_list:
                        #         client_list = experience.get("current_message", {}).get("client",[])
                        #         if client_list:
                        #             for client in client_list:
                        #                 await client_app.public_normal_company(client.get("data"))

                    else:
                        logger.error(f"未知解析错误 id->{gle_id} {res.status_code} {res.content}")
                else:
                    logger.info(f"解析错误 id->{gle_id} {res.status_code} {res.content}")
                    logger.info(res.content.decode())
                    continue


if __name__ == '__main__':
    while True:
        _gle_user_config = {
                "apiServerHost": "https://fsgtest.gllue.net",
                "aesKey": "824531e8cad2a287",
                "account": "api@fsg.com.cn"
            }
        _sync_config = {
                "entity": "candidate",
                "recent": "3",
                "unit": "day",
                "fieldName": "lastUpdateDate__lastUpdateDate__day_range",
                "gql": None,
            }
        asyncio.run(sync_candidate_pull_and_push(_gle_user_config,_sync_config))
        time.sleep(300)

