import asyncio
import os
import re
from asyncio import Task
from typing import Optional
from urllib.parse import urlencode
from urllib.parse import quote

import aiohttp
import jmespath
import requests
from pydantic import BaseModel

from channel.gllue.executor.push_job_order_tag.settings.settings import TipConfig
from channel.gllue.executor.push_job_order_tag.v4_function import FunctionV4ToGle
from utils.logger import logger


from channel.gllue.executor.model import GleUserConfig, SyncConfig
from channel.gllue.pull.application.applicaiton import GlePullApplication
from channel.gllue.pull.application.jobOrder.application import GleJobOrder
from channel.gllue.pull.application.jobSubMission.application import GleJobSubMissionInfo
from channel.gllue.pull.application.schema.application import GleSchema
from TipMidApp.application import TipMidApplication

from channel.gllue.push.application.application import GlePushApplication

settings = {"EntityStorageServerHost": os.getenv("EntityStorageServerHost", "http://localhost:9400"),
            "TipTagServerHost": os.getenv("TipTagServerHost", "http://effex.tpddns.cn:7777"),
            "TipJobParseServerHost": os.getenv("TipJobParseServerHost","http://localhost:54947")}

class ExtractMode(BaseModel):
    category: str
    tag: str

#
need_not_map_config = {
    "日薪金额": "gllueext_daily_wage",
    "时薪金额": "gllueext_hourly_wage",
    "工作地址": "gllueext_company_address",
    "工作时间": "gllueext_work_cycle",
}

need_convert_config = {
    "年龄上限": {"fieldName": ["gllueext_number_1690859067510"], "functionName": "get_int"},
    "年龄下限": {"fieldName": ["gllueext_number_1690859041960"], "functionName": "get_int"},
    "月薪和月薪月数": {"fieldName": ["monthlySalary", "maxMonthlySalary"],"functionName":"salary"},
    "工作城市":  {"fieldName": ["citys"], "functionName": "city"},
}

need_expand_map = {
     "学历要求": {
          "ExpandCategory": "education-fsg-gllue",
          "GllueTagName": "degree"
     },
     "工作年限要求": {
          "ExpandCategory": "experiences-fsg-gllue",
          "GllueTagName": "work_year"
     },
     "户籍要求": {
          "ExpandCategory": "huji-fsg-gllue",
          "GllueTagName": "gllueext_select_1690859746286"
     },
     "性别要求": {
          "ExpandCategory": "genders-fsg-gllue",
          "GllueTagName": "joborder_gllueext_select_1690859664815"
     }
}

async def push_job_order_tag_exec_v4(gle_user_config: GleUserConfig, sync_config: SyncConfig, tip_config:TipConfig):
    """
    同步谷露的职位(jobOrder)
    根据配置同步子关联实体[职位下候选人](jobSubMission)
    """
    async with aiohttp.ClientSession() as session:
        tip_app = TipMidApplication(session, settings)

        entity_name_list = ["joborder"]
        gle_pull_app = GlePullApplication(gle_user_config.dict(), sync_config.dict())
        schema_app: GleSchema = gle_pull_app.schema_app
        await schema_app.initialize_field_map_field("joborder")
        job_order_app: GleJobOrder = gle_pull_app.job_order_app
        gle_push_app = GlePushApplication(gle_user_config.dict())
        # 获取所有配置实体schema
        _schema_config: dict = {entity_name: await schema_app.get_schema(entity_name) for entity_name in entity_name_list}
        new_schema = {}
        for schema_name, schema_info in _schema_config.items():
            new_schema[schema_name] = ",".join([field_info["name"]for field_info in schema_info])
        schema_config = new_schema
        logger.info(f"获取到Schema的实体为->{list(schema_config.keys())}")
        # sync->gle-jobgllueext_monthpay_count
        job_order_task_list: Task = await job_order_app.sync()
        for task in asyncio.as_completed(job_order_task_list):
            job_list: list = await task
            # 同步到JobInfo
            for job_order in job_list:
                data, status = await tip_app.source_entity_storage_app.get_entity({"tenant": tip_config.tenant_alias, "source_entity_type": "JobOrder", "source_id": job_order["id"]})
                storage_data = [jmespath.search("description", data), jmespath.search("job_requirements", data)]
                gle_data = [jmespath.search("description", job_order), jmespath.search("job_requirements", job_order)]
                storage_data = [_ for _ in storage_data if _]
                gle_data = [_ for _ in gle_data if _]
                if not (gle_data != storage_data and gle_data):
                    logger.info(f"跳过job_order->{job_order['id']}")

                if gle_data != storage_data and gle_data:
                    pass
                if True:
                    func_app = FunctionV4ToGle()
                    texts = [_.replace("\n", "") for _ in gle_data if _]
                    logger.info(f"预备给job_order->{job_order['id']}打标签")
                    logger.info(texts)
                    job_parsed, _ = await tip_app.tip_job_parse_v2.parse({
                        "description": ",".join(texts)
                    })
                    job_parsed_spans: list = job_parsed["spans"]
                    logger.info(f"开始职位解析->{job_order['id']}")
                    for job_parsed_span in job_parsed_spans:
                        logger.info(job_parsed_span["entity"])
                        if (span_name := job_parsed_span["entity"]) and (span_name in ["SALARY", "WORK_TIME", "AGE", "LOCATION", "DEGREE"]):
                            if span_name == "SALARY":
                                func_app.job_parse_v2_salary_range_query(job_parsed_span["range_query"])
                            elif span_name == "WORK_TIME":
                                func_app.job_parse_v2_work_year_term(job_parsed_span["term_query"].get("term", {}))
                            elif span_name == "AGE":
                                logger.info(job_parsed_span)
                                func_app.job_parse_v2_age_range_query(job_parsed_span.get("range_query",{}).get("term", {}))
                            elif span_name == "LOCATION":
                                # func_app.job_parse_v2_age_range_query(job_parsed_span.get("range_query", {}).get("term", {}))
                                pass

                    # 学历、性别、年龄 薪资 地点 工作周期
                    job_parse_field = ["DEGREE", "GENDER", "AGE", "SALARY", "LOCATION", "WORK_TIME"]
                    job_parse_field = ["DEGREE", "GENDER", "AGE", "SALARY", "LOCATION", "WORK_TIME"]
                #         logger.info(f"维度结果->{extract_info_list}")
                #         extract_info_list = [ExtractMode(**i) for i in extract_info_list]
                #         for extract in extract_info_list:
                #             # 不需要映射的
                #             try:
                #                 if extract.category in need_not_map_config.keys():
                #                     new_gllue_body[need_not_map_config[extract.category]] = extract.tag
                #                 # 直接转换
                #                 elif extract.category in need_convert_config.keys():
                #                     total_config = need_convert_config[extract.category]
                #                     func_name = total_config["functionName"]
                #                     if func_name == "get_int":
                #                         if _r := re.search(r'\d+', extract.tag):
                #                             # 必须为1
                #                             new_gllue_body[total_config["fieldName"][0]] = _r.group()
                #                     elif func_name == "salary":
                #                         _r1 = tip_app.field_normalization_app.salary_range(extract.category)
                #                         _r1.get("gt", {}).get("months")
                #                         _r2 = [jmespath.search(jma, _r1) for jma in ["gt.months",'gt.amount.number',"lt.amount.number"]]
                #                         for field_name, _result in zip(total_config["fieldName"], _r2):
                #                             new_gllue_body[field_name] = _result
                #                     elif func_name == "city":
                #                         _id = schema_app.get_city_id_by_location_string(extract.category)
                #                         new_gllue_body[total_config["fieldName"][0]] = _id
                #
                #
                #                 # 需要抽取的
                #                 elif ex_total_config := need_expand_map.get(extract.category):
                #                     request_body = {
                #                         "texts": [extract.tag],
                #                         "output_category": ex_total_config["ExpandCategory"],
                #                     }
                #                     if extract.category in ["工作年限要求"]:
                #                         request_body["rerank"] = True
                #                     expand_tag = await tip_app.tip_tag_app.expand_flatten(request_body)
                #                     tag = expand_tag[0]["tag"]
                #                     logger.info(tag)
                #                     if extract.category == "学历要求":
                #                         new_gllue_body["degree"] = schema_app.field_string_map["joborder"]["degree"][tag]
                #
                #                     elif extract.category == "工作年限要求":
                #                         new_gllue_body["work_year"] = schema_app.field_string_map["joborder"]["work_year"][tag]
                #                     elif extract.category == "户籍要求":
                #                         new_gllue_body["gllueext_select_1690859746286"] = schema_app.field_string_map["joborder"]["gllueext_select_1690859746286"][
                #                             tag]
                #                     elif extract.category == "性别要求":
                #                         new_gllue_body["joborder_gllueext_select_1690859664815"] = schema_app.field_string_map["joborder"]["gllueext_select_1690859746286"][
                #                             tag]
                #             except Exception as e2:
                #                 logger.info(e2)
                #                 pass
                #         expand_tag_list = await tip_app.tip_tag_app.expand_flatten({
                #                 "texts": [job_order["jobTitle"]],
                #                 "output_category": "position3",
                #
                #             })
                #         new_gllue_body["function"] = schema_app.field_string_map["function"][expand_tag_list[0]["tag"]]
                #         logger.info(new_gllue_body)
                #         res = await gle_push_app.job_order_app.update_job_order_by_id(job_order_id=job_order["id"],overwrite_info=new_gllue_body)
                #         if res.get("status"):
                #             _data = await tip_app.source_entity_storage_app.put_entity(
                #                 {"tenant": tip_config.tenant_alias,
                #                  "source_entity_type": "JobOrder",
                #                  "source_id": job_order["id"],
                #                  "payload": {**job_order, **new_gllue_body}
                #                  })
                # except Exception as e:
                #     logger.error(f"出现错误，最后->{new_gllue_body}")
                #     res = await gle_push_app.job_order_app.update_job_order_by_id(job_order_id=job_order["id"],
                #                                                                   overwrite_info=new_gllue_body)
                #     logger.info(res)
                #     logger.error(e)
