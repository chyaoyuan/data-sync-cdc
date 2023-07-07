import asyncio

import requests
from loguru import logger

from channel.gllue.application.applicaiton import GlePullApplication


async def sync_candidate_pull_and_push():
    candidate_app = GlePullApplication({
                "apiServerHost": "https://fsgtest.gllue.net",
                "aesKey": "824531e8cad2a287",
                "account": "api@fsg.com.cn"
            }, {
                "entity": "candidate",
                "recent": "1",
                "unit": "year",
                "gql": None,
            }).candidate_app
    client_app = GlePullApplication({
        "apiServerHost": "https://fsgtest.gllue.net",
        "aesKey": "824531e8cad2a287",
        "account": "api@fsg.com.cn"
    },{
                "entity": "candidate",
                "recent": "1",
                "unit": "year",
                "gql": None,
            }).client_app
    await candidate_app.check_token()
    field_name_list: str = await candidate_app.initialize_field()
    max_page_index = await candidate_app.get_max_page()

    for index_page in range(1, max_page_index + 1):
        entity_list = await candidate_app.get_candidate_info(index_page, field_name_list)
        logger.info(f"第{index_page}页 entity->{candidate_app.entity} id->{[entity['id'] for entity in entity_list]}")
        for entity in entity_list:
            gle_id = entity["id"]
            entity["locations"] = str(entity["locations"])
            if gle_id == 333:

                logger.info(entity["locations"])
            if entity.get("attachment") or None:
                attachment_info_list = entity.get("attachment")
                attachment = attachment_info_list[0]
                headers = {
                    'Authorization': 'APPCODE ' + "085c11ede59c44588116918f0d3ee1ed",
                    'Content-Type': 'application/json; charset=UTF-8',
                }

                data = {
                    "file_name": attachment["fileName"],
                    "file_cont": attachment["fileContent"],
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
                        logger.info(gle_entity)
                        # company_name_list
                        job_title_list = list(set([_.get("title") for _ in gle_entity.get("candidateexperience_set",[]) if _.get("title",)]))
                        logger.info(job_title_list)
                        tags = []
                        for job_title in job_title_list:
                            payload = {
                                "texts": [
                                    job_title
                                ],
                                "field": "description",
                                "domain": "hr",
                                "output_category": "position3",
                                "top_k": 1
                            }
                            try:
                                response = requests.request("POST", "http://effex.tpddns.cn:7777/v1alpha1/tagging/expand", headers=headers, json=payload,timeout=5)
                                if response.status_code == 200:
                                    logger.info(response.json())
                                    tags.append(response.json()["tags"][0][0].get("tag"))
                                else:
                                    logger.error(f"标签解析失败->{response.status_code} {response.content.decode()}")
                            except requests.exceptions.ReadTimeout:
                                logger.error(f"标签服务超时跳过")
                        if tags:
                            gle_entity["tags"] = tags
                        info = await candidate_app.push_entity(gle_entity)
                        # get company id
                        if info:
                            experience_list = info.get("current_message", {}).get("candidateexperience", [])
                            for experience in experience_list:
                                client_list = experience.get("current_message", {}).get("client",[])
                                if client_list:
                                    for client in client_list:
                                        await client_app.public_normal_company(client.get("data"))

                    else:
                        logger.error(f"未知解析错误 id->{gle_id} {res.status_code} {res.content}")
                else:
                    logger.info(f"解析错误 id->{gle_id} {res.status_code} {res.content}")
                    logger.info(res.content.decode())
                    continue

async def sync_company_pull_and_push():
    candidate_app = GlePullApplication({
                "apiServerHost": "https://fsgtest.gllue.net",
                "aesKey": "824531e8cad2a287",
                "account": "api@fsg.com.cn"
            }, {
                "entity": "client",
                "recent": "1",
                "unit": "year",
                "gql": None,
            }).candidate_app
    client_app = GlePullApplication({
        "apiServerHost": "https://fsgtest.gllue.net",
        "aesKey": "824531e8cad2a287",
        "account": "api@fsg.com.cn"
    },{
                "entity": "client",
                "recent": "1",
                "unit": "year",
                "gql": None,
            }).client_app
    await candidate_app.check_token()
    field_name_list: str = await candidate_app.initialize_field()
    max_page_index = await candidate_app.get_max_page()

    for index_page in range(1, max_page_index + 1):
        entity_list = await candidate_app.get_candidate_info(index_page, field_name_list)
        logger.info(f"第{index_page}页 entity->{candidate_app.entity} id->{[entity['id'] for entity in entity_list]}")
        for entity in entity_list:
            gle_id = entity["id"]
            logger.info(entity)
            company_name = entity["name"]
            payload = {
                "texts": [
                    company_name
                ],
                "field": "company",
                "domain": "hr",
                "output_category": "industry",
                "top_k": 1
            }
            try:
                response = requests.request("POST", "http://effex.tpddns.cn:7777/v1alpha1/tagging/expand", json=payload, timeout=10)
                if response.status_code == 200:
                    tag = response.json()["tags"][0][0].get("tag")
                    await client_app.public_company_tag(gle_id, tag)
                else:
                    logger.error(f"标签解析失败->{response.status_code} {response.content.decode()}")
            except requests.exceptions.ReadTimeout:
                logger.error(f"标签服务超时跳过")

if __name__ == '__main__':
    asyncio.run(sync_company_pull_and_push())

