import traceback

from channel.gllue.executor.push_candidate_tag.app import TipTagApp
from channel.gllue.executor.push_job_order_tag.settings.settings import TipConfig
from datetime import datetime
import os
import aiohttp
import jmespath
from TipMidApp import TipMidApplication
from loguru import logger
from channel.gllue.pull.application.applicaiton import GlePullApplication
from channel.gllue.push.application.application import GlePushApplication
from channel.gllue.executor.model import GleUserConfig, SyncConfig


def count_years(date_ranges):
    total_years = 0
    for date_range in date_ranges:
        try:
            start_date = datetime.strptime(date_range["start_date"], "%Y.%m")

            if date_range["end_date"] == "至今":
                end_date = datetime.now()
            else:
                end_date = datetime.strptime(date_range["end_date"], "%Y.%m")

            delta = end_date - start_date
            total_years += delta.days / 365.0  # 将天数转换为年数并累加
        except Exception as e:
            pass
    return total_years


settings = {
    "EntityStorageServerHost": os.getenv("EntityStorageServerHost", "http://localhost:9400"),
     "TipTagServerHost": os.getenv("TipTagServerHost", "https://effex-actions.nadileaf.com"),
     "ResumeSDKServerHost": os.getenv("TipTagServerHost", "http://resumesdk.market.alicloudapi.com"),
     "ConvertServerHost": os.getenv("ConvertServerHost", "http://converter.nadileaf.com")
}


async def execute(tip_tag_app,gle_entity_id,entity,tip_app,schema_app,candidate_push_app,tip_config,candidate_pull_app):
    logger.info(f"谷露->{gle_entity_id}执行运行")
    latest_resume_info = entity.get("mesoorExtraLatestResume")
    resume_sdk_candidate = await tip_app.resume_sdk_app.parse(latest_resume_info["fileName"],
                                                              latest_resume_info["fileContent"])
    if not resume_sdk_candidate:
        logger.info(f"pass->{gle_entity_id}")
        return
    # logger.info(resume_sdk_candidate)
    gle_resume, _ = await tip_app.convert_app.convert("Resumegl:standard:2023_07_03_09_34_35", resume_sdk_candidate)
    logger.info(f"gllue-resume->{gle_resume}")
    # 给简历打标签
    resume_tag = get_jme_s_path_batch(
        ["lang_objs[].language_name", "cert_objs[].langcert_name", "cert_objs[].langcert_name",
         "cert_objs[].langcert_name", "cert_objs[].langcert_name", "cert_objs[].langcert_name",
         "cert_objs[].langcert_name", "cert_objs[].langcert_name", "skills_objs[].skills_name"], resume_sdk_candidate)
    logger.info(f"gllue-resume-tag->{resume_tag}")
    gle_resume["tags"] = resume_tag
    # 职位名标签
    # 获取职位名
    position_name_list: list = get_jme_s_path_batch(["job_exp_objs[].job_position"], resume_sdk_candidate)
    logger.info(position_name_list)
    position_name_list = [i for i in position_name_list if i]
    duty_tag_list = []
    if position_name_list:
        for position_name in position_name_list:
            duty_tag_info_list = await tip_tag_app.expand_flatten(
                {"texts": [position_name], "output_category": "position3", "top_k": 1, "rerank":True})
            if not duty_tag_info_list:
                logger.info("重新排序失败")
                duty_tag_info_list = await tip_tag_app.expand_flatten(
                    {"texts": [position_name], "output_category": "position3", "top_k": 1})
            if duty_tag_info_list:
                for duty_tag_info in duty_tag_info_list:
                    duty_tag_list.append(duty_tag_info["tag"])


    gle_resume["tags"] = gle_resume["tags"] + duty_tag_list
    logger.info(f"duty_tag_list->{duty_tag_list}")
    # 行业
    company_name_list: list = get_jme_s_path_batch(["job_exp_objs[].job_cpy"], resume_sdk_candidate)
    industry_tag_list = []
    logger.info(f"company_name_list->{company_name_list}")
    if company_name_list:
        for company_name in company_name_list:
            industry_tag_info_list = await tip_tag_app.expand_flatten(
                {"texts": [company_name], "output_category": "industry2-hr", "top_k": 1, "rerank": True})
            if not industry_tag_info_list:
                logger.info("重新排序失败")
                industry_tag_info_list = await tip_tag_app.expand_flatten(
                    {"texts": [company_name], "output_category": "industry2-hr", "top_k": 1})
            if industry_tag_info_list:
                for industry_tag_info in industry_tag_info_list:
                    industry_tag_list.append(industry_tag_info["tag"])
    gle_resume["tags"] = gle_resume["tags"] + industry_tag_list
    logger.info(f"industry_tag_list->{industry_tag_list}")
    industry_tag_id = []
    for industry_tag_name in industry_tag_list:
        if industry_id := schema_app.field_string_map["industry"].get(industry_tag_name):
            industry_tag_id.append(str(industry_id))

    logger.info(industry_tag_id)
    industry_tag_id_str = ",".join(list(set(industry_tag_id)))


    duty_tag_id = []
    for duty_tag in duty_tag_list:
        if tag_id := schema_app.field_string_map["function"].get(duty_tag):
            duty_tag_id.append(str(tag_id))
    duty_tag_id_str = ",".join(list(set(duty_tag_id)))
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
    if college_type_list:
        if [int(college_type_id) for college_type_id in college_type_list]:
            max_college_type = max([int(college_type_id) for college_type_id in college_type_list])
            gle_resume["tags"].append(college_type_map.get(max_college_type))
    time_list = [{"start_date": i.get("start_date"), "end_date": i.get("end_date")} for i in
                 resume_sdk_candidate.get("job_exp_objs", []) if i.get("start_date") and i.get("end_date")]
    work_years = count_years(time_list)
    if work_years > 5:
        gle_resume["tags"].append("五年以上工作经验")

    logger.info(f"共计工作多少年->{work_years}")

    gle_resume["tags"] = gle_resume["tags"]
    logger.info(gle_resume)
    info = await candidate_push_app.push_candidate(gle_resume)
    if info:
        await tip_app.source_entity_storage_app.put_entity(
            {"tenant": tip_config.tenant_alias, "source_entity_type": "GllueCandidate", "source_id": gle_entity_id,
             "payload": candidate_pull_app.pop_entity_file_content(entity)})

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


async def push_candidate_tag_v3(gle_user_config: GleUserConfig, sync_config: SyncConfig, tip_config: TipConfig):
    async with aiohttp.ClientSession() as session:
        gle_pull_app = GlePullApplication(gle_user_config.dict(), sync_config.dict())
        tip_tag_app = TipTagApp(session, settings)
        candidate_pull_app = gle_pull_app.candidate_app
        schema_app = gle_pull_app.schema_app
        await schema_app.initialize_field_map_field("candidate")
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
                old_entity, status = await tip_app.source_entity_storage_app.get_entity({"tenant": tip_config.tenant_alias,"source_entity_type":"GllueCandidate","source_id": gle_entity_id})
                old_entity = old_entity if old_entity else {}
                old_entity_last_resume_uuid = old_entity.get("mesoorExtraLatestResume", {}).get("uuidname", )
                new_entity_last_resume_uuid = entity.get("mesoorExtraLatestResume", {}).get("uuidname")
                signal = False
                if not old_entity_last_resume_uuid:
                    logger.info(f"gle_entity_id->{gle_entity_id} 没有同步过执行同步")
                    signal = True
                elif old_entity_last_resume_uuid and old_entity_last_resume_uuid != new_entity_last_resume_uuid:
                    logger.info(f"gle_entity_id->{gle_entity_id} 被更新执行同步")
                    signal = True

                if signal and (entity.get("mesoorExtraLatestResume") or None):
                    try:
                        await execute(tip_tag_app, gle_entity_id,entity,tip_app,schema_app,candidate_push_app,tip_config,candidate_pull_app)
                    except Exception as e:
                        traceback.print_exc()
                        continue
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
