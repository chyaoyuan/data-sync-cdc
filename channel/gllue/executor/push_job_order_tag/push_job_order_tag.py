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
from utils.logger import logger


from channel.gllue.executor.model import GleUserConfig, SyncConfig, TipConfig
from channel.gllue.pull.application.applicaiton import GlePullApplication
from channel.gllue.pull.application.jobOrder.application import GleJobOrder
from channel.gllue.pull.application.jobSubMission.application import GleJobSubMissionInfo
from channel.gllue.pull.application.schema.application import GleSchema
from TipMidApp.application import TipMidApplication

from channel.gllue.push.application.application import GlePushApplication

settings = {"entityStorageServerHost": os.getenv("EntityStorageServerHost", "http://localhost:9400"),
            "TipTagServerHost": os.getenv("TipTagServerHost", "http://effex.tpddns.cn:7777")}


async def push_job_order_tag_exec(gle_user_config: GleUserConfig, sync_config: SyncConfig):
    """
    同步谷露的职位(jobOrder)
    根据配置同步子关联实体[职位下候选人](jobSubMission)
    """
    async with aiohttp.ClientSession() as session:
        tip_app = TipMidApplication(session, settings)
        pull_test = True
        # gle 同步基础
        # 获取所有需要同步的实体名
        entity_name_list: list = [entity.entityName for entity in sync_config.childEntityList]
        entity_name_list.append("joborder")
        entity_name_list: list = list(set(entity_name_list))
        # 运行应用
        gle_pull_app = GlePullApplication(gle_user_config.dict(), sync_config.dict())

        schema_app: GleSchema = gle_pull_app.schema_app

        job_order_app: GleJobOrder = gle_pull_app.job_order_app
        gle_push_app = GlePushApplication(gle_user_config.dict())
        # 获取所有配置实体schema
        _schema_config: dict = {entity_name: await schema_app.get_schema(entity_name) for entity_name in entity_name_list}

        new_schema = {}
        for schema_name, schema_info in _schema_config.items():
            new_schema[schema_name] = ",".join([field_info["name"]for field_info in schema_info])
        schema_config = new_schema
        logger.info(f"获取到Schema的实体为->{list(schema_config.keys())}")
        # sync->gle-job
        job_order_task_list: Task = await job_order_app.sync()
        for task in asyncio.as_completed(job_order_task_list):
            job_list: list = await task
            # 同步到JobInfo
            for job_order in job_list:
                # data, status = await tip_app.source_entity_storage_app.get_entity({"tenant": "tenant", "source_entity_type": "JobOrder", "source_id": job_order["id"]})
                # storage_data = [jmespath.search("description", data), jmespath.search("job_requirements", data)]
                gle_data = [jmespath.search("description", job_order), jmespath.search("job_requirements", job_order)]
                # storage_data = [_ for _ in storage_data if _]
                # gle_data = [_ for _ in gle_data if _]
                # #

                # if gle_data != storage_data and gle_data:
                if True:
                    # todo 打维度
                    texts = [_.replace("\n", "") for _ in gle_data if _]
                    logger.info(f"预备给job_order->{job_order['id']}打标签")
                    extract_tag_list, status = await tip_app.tip_tag_app.extract_flatten({
                        "texts": texts,
                        "field": "description",
                        "domain": "hr",
                        "output_category": "工作城市|工作地址|月薪和月薪月数|日薪金额|时薪金额|工作时间|学历要求|工作年限要求|年龄下限|年龄上限|户籍要求｜性别要求",
                        "top_k": 1
                    })
                    if status != 200:
                        logger.error(extract_tag_list)
                        continue
                    else:
                        logger.info(f"维度结果为->{extract_tag_list}")

                        config = {
                            "日薪金额": "gllueext_daily_wage",
                            "时薪金额": "gllueext_hourly_wage",
                            "工作地址": "gllueext_company_address",
                            "工作时间": "gllueext_work_cycle",
                        }
                        linshi = {}
                        job_order_update_info = {}
                        # job_order_update_info["interview_process"] = extract_tag_list
                        for tag in extract_tag_list:
                            if tag["category"] in config.keys():
                                job_order_update_info[config[tag["category"]]] = tag["tag"]
                            if tag["category"] == "年龄上限":
                                c2 = re.search(r'\d+', tag["tag"])
                                if c2:
                                    job_order_update_info["gllueext_number_1690859067510"] = c2.group()
                            elif tag["category"] == "年龄下限":
                                c1 = re.search(r'\d+', tag["tag"])
                                if c1:
                                    job_order_update_info["gllueext_number_1690859041960"] = c1.group()
                            elif tag["category"] == "月薪和月薪月数":
                                rees = tip_app.field_normalization_app.salary_range(tag["tag"])
                                job_order_update_info["gllueext_monthpay_count"] = rees.get("gt", {}).get("months")
                                job_order_update_info["monthlySalary"] = rees.get("gt", {}).get("amount", {}).get(
                                    "number")
                                job_order_update_info["maxMonthlySalary"] = rees.get("lt", {}).get("amount",
                                                                                                       {}).get("number")
                        c = [
                            {"ExtractCategory": "学历要求",
                             "ExpandCategory": "education-fsg-gllue",
                             "GllueTagName": "degree"},
                            {"ExtractCategory": "工作年限要求",
                             "ExpandCategory": "experiences-fsg-gllue",
                             "GllueTagName": "work_year"},
                            {"ExtractCategory": "工作城市",
                             "Func": True,
                             "GllueTagName": "citys"},
                            {"ExtractCategory": "户籍要求",
                             "ExpandCategory": "huji-fsg-gllue",
                             "GllueTagName": "gllueext_select_1690859746286"},
                            {"ExtractCategory": "性别要求",
                             "ExpandCategory": "genders-fsg-gllue",
                             "GllueTagName": "joborder_gllueext_select_1690859664815"},

                        ]
                        for tag in extract_tag_list:
                            if tag and tag["category"] in [i["ExtractCategory"]for i in c]:

                                c_total_config = get_(c, tag["category"])
                                if not c_total_config.get("Func"):
                                    logger.info(tag)
                                    expand_tag_list, status = await tip_app.tip_tag_app.expand_flatten({
                                        "texts": [tag["tag"]],
                                        "field": "description",
                                        "domain": "hr",
                                        "output_category": c_total_config["ExpandCategory"],
                                        "top_k": 1
                                    })
                                    if status != 200:
                                        continue
                                    for _tag in expand_tag_list:
                                        linshi[f"MesoorExtra{c_total_config['GllueTagName']}"] = _tag["tag"]
                                else:
                                    if tag["category"] == "工作城市":
                                        gle_location_id = schema_app.get_city_id_by_location_string(tag["tag"])
                                        job_order_update_info["citys"] = gle_location_id

                                logger.info(linshi)
                                logger.info(_schema_config)
                                for k, v in linshi.items():
                                    if "MesoorExtra" in k:
                                        if "degree" in k:
                                            job_order_update_info["degree"] = schema_app.degree_map[v]
                                        elif "work_year" in k:
                                            job_order_update_info["work_year"] = schema_app.work_year_map.get(v)
                                        elif "gllueext_select_1690859746286" in k:
                                            job_order_update_info["gllueext_select_1690859746286"] = get__(_schema_config["joborder"], "gllueext_select_1690859746286")[v]
                                        elif "gllueext_select_1690859664815" in k:
                                            job_order_update_info["gllueext_select_1690859664815"] = get__(_schema_config["joborder"], "gllueext_select_1690859664815")[v]

                        try:
                            expand_tag_list, status = await tip_app.tip_tag_app.expand_flatten({
                                "texts": [job_order["jobTitle"]],
                                "field": "description",
                                "domain": "hr",
                                "output_category": "position3",
                                "top_k": 1
                            })
                            logger.info(expand_tag_list)
                            logger.info(schema_app.field_string_map)
                            job_order_update_info["function"] = schema_app.field_string_map["function"][expand_tag_list[0]["tag"]]
                        except Exception as e:
                            logger.error(e)
                        if len(job_order_update_info) >= 1:
                            await gle_push_app.job_order_app.update_job_order_by_id(job_order_id=job_order["id"], overwrite_info=job_order_update_info)
                        # _data = await tip_app.source_entity_storage_app.put_entity(
                        #     {"tenant": "tenant",
                        #      "source_entity_type": "JobOrder",
                        #      "source_id": job_order["id"],
                        #      "payload": {**job_order, **job_order_update_info}
                        #      })





