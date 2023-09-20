import asyncio
import time
import jmespath
import requests
import os
from utils.logger import logger
from channel.gllue.executor.push_job_order_tag.settings.settings import TipConfig
from datetime import datetime
from channel.gllue.pull.application.applicaiton import GlePullApplication
from channel.gllue.executor.config import gllue_industry_config_map, gllue_zhienng_config_map
from channel.gllue.push.application.application import GlePushApplication

def count_years(date_ranges):
    total_years = 0
    for date_range in date_ranges:
        start_date = datetime.strptime(date_range["start_date"], "%Y.%m")

        if date_range["end_date"] == "至今":
            end_date = datetime.now()
        else:
            end_date = datetime.strptime(date_range["end_date"], "%Y.%m")

        delta = end_date - start_date
        total_years += delta.days / 365.0  # 将天数转换为年数并累加
    return total_years

settings = {"EntityStorageServerHost": os.getenv("EntityStorageServerHost", "http://localhost:9400"),
            "TipTagServerHost": os.getenv("TipTagServerHost", "http://effex.tpddns.cn:7777")}


def get_jme_s_path_batch(jme_s_path_list: list[str], data: dict):
    result_list = []
    for jme_s_path in jme_s_path_list:
        result = jmespath.search(jme_s_path, data)
        if isinstance(result, list):
            for _ in result:
                result_list.append(_)
        elif isinstance(result, str):
            result_list.append(result)
        else:
            logger.error("未定义的类型")
    return list(set(result_list))




import os

import aiohttp
import jmespath
from TipMidApp import TipMidApplication
from loguru import logger

from channel.gllue.pull.application.applicaiton import GlePullApplication
from channel.gllue.push.application.application import GlePushApplication
from channel.gllue.executor.model import GleUserConfig, SyncConfig
settings = {"EntityStorageServerHost": os.getenv("EntityStorageServerHost", "http://localhost:9400"),
            "TipTagServerHost": os.getenv("TipTagServerHost", "http://effex.tpddns.cn:7777"),
            "ResumeSDKServerHost":os.getenv("TipTagServerHost", "http://resumesdk.market.alicloudapi.com"),
            "ConvertServerHost": os.getenv("ConvertServerHost", "http://converter.nadileaf.com")}


async def push_candidate_tag_v3(gle_user_config: GleUserConfig, sync_config: SyncConfig, tip_config: TipConfig):
    async with aiohttp.ClientSession() as session:
        gle_pull_app = GlePullApplication(gle_user_config.dict(), sync_config.dict())
        candidate_pull_app = gle_pull_app.candidate_app
        schema_app = gle_pull_app.schema_app
        await schema_app.initialize_field_map_field("joborder")
        candidate_push_app = GlePushApplication(gle_user_config.dict()).candidate_app
        tip_app = TipMidApplication(session, settings)
        field_name_list: str = await candidate_pull_app.initialize_field()
        page_total = await candidate_pull_app.get_max_page()
        for index_page in range(1, page_total + 1):
            entity_list, _ = await candidate_pull_app.get_candidate_info(index_page, field_name_list)

            logger.info(f"第{index_page}页 entity->{candidate_pull_app.entityType} id->{[entity['id'] for entity in entity_list]}")
            for entity in entity_list:
                gle_entity_id = entity["id"]
                # 判断变动
                # old_entity, status = await tip_app.source_entity_storage_app.get_entity({"tenant": tip_config.tenant_alias,"source_entity_type":"Candidate","source_id": gle_id})
                # if status == 200 and old_entity.get("latestResume") and entity.get("latestResume"):
                # if False:
                #     pass
                #     # old_entity_last_resume = old_entity.get("latestResume")
                #     # new_entity_last_resume = entity.get("latestResume")
                #     # if old_entity_last_resume == new_entity_last_resume:
                #     #     logger.info(f"gle {gle_id}没有更新简历附件 跳过")
                #     #     continue
                if entity.get("latestResume") or None:
                    latest_resume_info = entity.get("latestResume")
                    resume_sdk_candidate = await tip_app.resume_sdk_app.parse(latest_resume_info["fileName"], latest_resume_info["fileContent"])
                    logger.info(f"ResumeSDK-Resume->{resume_sdk_candidate}")
                    gle_resume, _ = await tip_app.convert_app.convert("Resumegl:standard:2023_07_03_09_34_35", resume_sdk_candidate)
                    logger.info(f"gllue-resume->{gle_resume}")
                    # 给简历打标签
                    resume_tag = get_jme_s_path_batch(["lang_objs[].language_name", "cert_objs[].langcert_name","cert_objs[].langcert_name","cert_objs[].langcert_name","cert_objs[].langcert_name","cert_objs[].langcert_name","cert_objs[].langcert_name","cert_objs[].langcert_name","skills_objs[].skills_name"],resume_sdk_candidate)
                    logger.info(f"gllue-resume-tag->{resume_tag}")
                    gle_resume["tags"] = resume_tag
                    # 职位名标签
                    # 获取职位名
                    position_name_list: list = get_jme_s_path_batch(["job_exp_objs[].job_position"], resume_sdk_candidate)
                    duty_tag_info_list = await tip_app.tip_tag_app.expand_flatten(
                        {"texts": [','.join(position_name_list)], "output_category": "position3","top_k": 3})
                    logger.info(f"duty_tag_list->{duty_tag_info_list}")
                    duty_tag_list = [duty_tag_info["tag"] for duty_tag_info in duty_tag_info_list]
                    logger.info(f"duty_tag_list->{duty_tag_list}")
                    # 行业
                    company_name_list: list = get_jme_s_path_batch(["job_exp_objs[].job_cpy"], resume_sdk_candidate)
                    logger.info(f"company_name_list->{company_name_list}")
                    industry_tag_info_list = await tip_app.tip_tag_app.expand_flatten({"texts": [','.join(company_name_list)], "output_category": "industry2-hr", "top_k": 3})
                    logger.info(f"industry_tag_info_list->{industry_tag_info_list}")
                    industry_tag_list = [industry_tag_info["tag"] for industry_tag_info in industry_tag_info_list]
                    logger.info(f"industry_tag_list->{industry_tag_list}")
                    industry_tag_id = []
                    for industry_tag_name in industry_tag_list:
                        industry_tag_id.append(str(schema_app.field_string_map["industry"][industry_tag_name]))

                    logger.info(industry_tag_id)
                    industry_tag_id_str = ",".join(industry_tag_id)
                    logger.info(industry_tag_id)

                    duty_tag_id = []
                    for duty_tag in duty_tag_list:
                        duty_tag_id.append(str(schema_app.field_string_map["function"][duty_tag]))
                    duty_tag_id_str = ",".join(duty_tag_id)
                    logger.info(duty_tag_id_str)

                    gle_resume["id"] = gle_entity_id
                    gle_resume["industrys"] = industry_tag_id_str
                    gle_resume["functions"] = duty_tag_id_str
                    logger.info(gle_resume)
                    edu_recruit_name_list: list = get_jme_s_path_batch(["education_objs[].edu_recruit"], resume_sdk_candidate)
                    for edu_recruit_name in edu_recruit_name_list:
                        if edu_recruit_name in ["自考", "在职", "成教", "函授"]:
                            gle_resume["tags"].append("非全日制")
                    edu_degree_name_list: list = get_jme_s_path_batch(["education_objs[].edu_degree"], resume_sdk_candidate)
                    for edu_degree_name in edu_degree_name_list:
                        if edu_degree_name in ["研究生", "硕士", "博士", "博士后", "mba"]:
                            gle_resume["tags"].append("硕/博士")
                    if (has_oversea_edu := resume_sdk_candidate.get("has_oversea_edu")) and (has_oversea_edu == "1"):
                        gle_resume["tags"].append("海外留学")
                    college_type_map = \
                        {0: "普通院校",
                        1: "985",
                        2: "211",
                        3: "港澳台院校",
                        4: "海外院校",
                        5: "中学",
                        6: "职业教育",
                        7: "培训机构"}
                    college_type_list = get_jme_s_path_batch(["education_objs[].edu_college_type"], resume_sdk_candidate)
                    logger.info([int(college_type_id) for college_type_id in college_type_list])
                    max_college_type = max([int(college_type_id) for college_type_id in college_type_list])
                    gle_resume["tags"].append(college_type_map.get(max_college_type))
                    time_list = [{"start_date":i.get("start_date"),"end_date":i.get("end_date") }for i in resume_sdk_candidate.get("job_exp_objs",[]) if i.get("start_date") and i.get("end_date")]
                    work_years = count_years(time_list)
                    if work_years>5:
                        gle_resume["tags"].append("五年以上工作经验")

                    logger.info(f"共计工作多少年->{work_years}")


                    info = await candidate_push_app.push_candidate(gle_resume)

                    if info:
                        pass
                        # 写回成功
                        await tip_app.source_entity_storage_app.put_entity(
                            {"tenant": "wf-test", "source_entity_type": "candidate", "source_id": gle_entity_id,
                             "payload": entity})

#
# if __name__ == '__main__':
#     while True:
#         _gle_user_config = {
#                 "apiServerHost": "https://fsgtest.gllue.net",
#                 "aesKey": "824531e8cad2a287",
#                 "account": "api@fsg.com.cn"
#             }
#         _sync_config = {
#                 "entity": "candidate",
#                 "recent": "3",
#                 "unit": "day",
#                 "fieldName": "lastUpdateDate__lastUpdateDate__day_range",
#                 "gql": None,
#             }
#         asyncio.run(sync_candidate_pull_and_push(_gle_user_config,_sync_config))
#         time.sleep(300)
#
