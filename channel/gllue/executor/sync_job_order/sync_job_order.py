import asyncio
import json
from asyncio import Task
from typing import Optional
from urllib.parse import urlencode
from urllib.parse import quote
import requests
from utils.logger import logger

from channel.gllue.executor.model import GleUserConfig, SyncConfig, TipConfig
from channel.gllue.pull.application.applicaiton import GlePullApplication
from channel.gllue.pull.application.jobOrder.application import GleJobOrder
from channel.gllue.pull.application.jobSubMission.application import GleJobSubMissionInfo
from channel.gllue.pull.application.schema.application import GleSchema
from middleware.external.application import external_application
from middleware.storage.application import tip_space_application


async def sync_gle_job_executor(gle_user_config: GleUserConfig, sync_config: SyncConfig, tip_config: TipConfig):
    """
    同步谷露的职位(jobOrder)
    根据配置同步子关联实体[职位下候选人](jobSubMission)
    """
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
    # 获取所有配置实体schema
    schema_config: dict = {entity_name: await schema_app.get_schema(entity_name) for entity_name in entity_name_list}
    new_schema = {}
    for schema_name, schema_info in schema_config.items():
        new_schema[schema_name] = ",".join([field_info["name"]for field_info in schema_info])
    schema_config = new_schema
    logger.info(f"获取到Schema的实体为->{list(schema_config.keys())}")
    # 根据配置是否启用子实体应用
    # 职位下候选人应用
    job_sub_mission_app: Optional[GleJobSubMissionInfo] = gle_pull_app.job_sub_mission_app if "jobSubMission" in entity_name_list else None

    # tip->channel
    # 不要url编码否则
    tip_channel_id = gle_user_config.account
    # sync->gle-job
    job_order_task_list: Task = await job_order_app.sync()
    for task in asyncio.as_completed(job_order_task_list):
        job_list: list = await task

        for job in job_list:
            job_sub_mission_id_list_log = []
            job_sub_mission_list_log = []
            candidate_id_list_log = []
            # await job_order_app.get_job_order_status(job["id"])
            # job转换
            if not pull_test:
                job_std_list: list = await external_application.convert_app.convert({"task_ids": [sync_config.convertId], "data":[{"sourceData":job}]})
                tip_project_id = tip_job_openid = f"gllue-jobSubMission-{tip_config.tenantAlias}-{job['id']}"
                await external_application.transmitter_app.save_data({
                    "tenant": tip_config.tenantAlias,
                    "entityType": "Job",
                    "entityId": tip_job_openid,
                    "entity": {
                        "standardFields": job_std_list[0],
                        "rawData": {
                            "content": {"sourceData": job}
                        }
                    },
                    "source": "gllue-new-job",
                    "editor": "data-sync-cdc",
                })


            job_sub_mission_task_list: Task = await job_sub_mission_app.sync_job_submission_by_job_order_id(job['id'], schema_config["jobSubMission"])
            for job_sub_mission_task in asyncio.as_completed(job_sub_mission_task_list):
                job_sub_mission_list = await job_sub_mission_task
                for index, job_sub_mission in enumerate(job_sub_mission_list):
                    job_sub_mission_id_list_log.append(job_sub_mission['id'])
                    candidate_id_list_log.append(job_sub_mission['candidate'])
                    job_sub_mission_list_log.append(job_sub_mission)
                    tip_resume_openid = f"gllue-candidate-{job_sub_mission['id']}"
                    # if not pull_test:
                    #     await external_application.transmitter_app.save_data({
                    #         "tenant": tip_config.tenantAlias,
                    #         "entityType": "Resume",
                    #         "entityId": tip_resume_openid,
                    #         "entity": {
                    #             "standardFields": {
                    #                 "name": job_sub_mission["__name__"],
                    #                 "humanInfo": job_sub_mission["__name__"]
                    #             },
                    #             "rawData": {
                    #                 "content": {"sourceData": job_sub_mission}
                    #             }
                    #         },
                    #         "source": "gllue-new-job-sub-mission",
                    #         "editor": "data-sync-cdc",
                    #     })


                # logger.info({"JobID": job['id'], "TotalSubMission": len(job_sub_mission_id_list),"TotalCandidate":len(candidate_id_list),"CandidateIDList":candidate_id_list,"SubMissionIDList":job_sub_mission_id_list})
            with open("job_order_and_job_sub_mission.jsonl","a") as f:
                f.write(json.dumps(
                    {"JobOrder": job,
                     "JobSubMissionList": job_sub_mission_list_log,
                     "logger": {"JobID": job['id'], "TotalSubMission":len(job_sub_mission_id_list_log),"TotalCandidate":len(candidate_id_list_log),"CandidateIDList":candidate_id_list_log,"SubMissionIDList":job_sub_mission_id_list_log}
                     }, ensure_ascii=False

                )+"\n")
            # headers = {
            #     'accept': 'application/json',
            #     # 'Tenant-Id': tip_config.tenantAlias,
            #     # 'User-Id': tip_config.userId,
            #     'Authorization': tip_config.Authorization,
            #     'Content-Type': 'application/json'
            # }
            body = {
                "space": {
                    "name": "谷露数据同步",
                    "openId": "gllue-data-sync"
                },
                "channel": {
                    "name": gle_user_config.account,
                    "openId": tip_channel_id
                },
                "project": {
                    "name": job_std_list[0]["name"],
                    "openId": tip_project_id
                },
                "entityType": "Job",
                "openId": tip_job_openid,
                "taskPayloadType": "Resume",
                "flowStages": [
                    {
                        "name": "Apply",
                    },
                    {
                        "name": "Screened",
                    },
                    {
                        "name": "Follow up",
                    },
                    {
                        "name": "Present to Consultant"
                    }

                ]
            }
            # res = requests.post(f"https://mesoor-space.nadileaf.com/v1/spaces/trees", headers=headers,json=body)
            # logger.info(res.status_code)
            # logger.info(res.text)




