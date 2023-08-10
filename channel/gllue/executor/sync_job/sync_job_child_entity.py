import asyncio
from asyncio import Task
from urllib.parse import urlencode
from urllib.parse import quote
import requests
from loguru import logger

from channel.gllue.pull.application.applicaiton import GlePullApplication
from middleware.external.application import external_application
from middleware.storage.application import tip_space_application






_sync_config = {
        "entity": "jobOrder",
        "recent": "3",
        "unit": "day",
        "fieldName": "lastUpdateDate__lastUpdateDate__day_range",
        "gql": "jobStatus__s=Live",
        "childEntityList": [{
            "gql": None,
            "entityName": "jobSubMission"
        }],


    }
_gle_user_config = {
                "apiServerHost": "https://fsgtest.gllue.net",
                "aesKey": "824531e8cad2a287",
                "account": "api@fsg.com.cn"
            }

_gle_user_config = {
                "apiServerHost": "https://www.cgladvisory.com",
                "aesKey": "eae48bfe137cc656",
                "account": "system@wearecgl.com"
            }
tip_config = {
    "jwtToken": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VybmFtZTo4NjE3NjEyMzA1NzE2IiwidGVuYW50SWQiOjYyODIsImlzcyI6ImRlZmF1bHQiLCJ0ZW5hbnRBbGlhcyI6ImFnOTM2Mjgya3pxZW0iLCJleHAiOjE2OTI3ODA2NjIwMjIsInVzZXJJZCI6IjJhOGZmNjE2LTZlMTQtNDQ2MS04YjRkLTJhM2ZkZDAxOTMzNyIsInByb2plY3RJZCI6ImRlZmF1bHQiLCJpYXQiOjE2OTE1NzEwNjIwMjJ9.KXY0ZsuTCYBiGv4vaz1gEwlJEMHo_E8Y8WDP7Sf2gTo",
    "spaceId": "fb6b3b31-2c2c-4e5f-9363-d51c6720d999",
    "tenantId": ""

}


async def gle_sync_executor():
    # gle 同步基础
    child_entity_field_name_list: list = [entity["entityName"].lower() for entity in _sync_config["childEntityList"]]
    gle_pull_app = GlePullApplication(_gle_user_config, _sync_config)
    schema_app = gle_pull_app.schema_app
    job_order_app = gle_pull_app.job_order_app
    schema_config: dict = {entity_name: await schema_app.get_schema(entity_name) for entity_name in child_entity_field_name_list}
    job_sub_mission_app = gle_pull_app.job_sub_mission_app if "jobSubMission".lower() in child_entity_field_name_list else None
    # tip同步基础 复用zyh
    # tip->渠道
    tip_channel_id = quote(_gle_user_config["account"])
    # await tip_space_application.channel_app.save_channel(
    #     {"channelId": tip_channel_id,
    #      "spaceId": tip_config["spaceId"],
    #      "name": _gle_user_config["account"],
    #      }, tip_config["jwtToken"]
    #         )

    job_order_task_list: Task = await job_order_app.run()
    for task in asyncio.as_completed(job_order_task_list):
        job_list: list = await task
        # 同步到JobInfo
        for job in job_list:
            # job转换
            std_list: list = await external_application.convert_app.convert({"task_ids": ["Job:standard:2023_04_10_02_43_42"], "data":[{"sourceData":job}]})
            tip_job_openid = f"gllue-jobSubMission-{job['id']}"
            print(job)
            # await external_application.transmitter_app.save_data({
            #     "tenant": "ag936282kzqem",
            #     "entityType": "Job",
            #     "entityId": tip_job_openid,
            #     "entity": {
            #         "standardFields": std_list[0],
            #         "rawData": {
            #             "content": {"sourceData": job}
            #         }
            #     },
            #     "source": "gllue-new-job",
            #     "editor": "data-sync-cdc",
            # })
            # headers = {
            #     'accept': 'application/json',
            #     'Tenant-Id': 'ag936282kzqem',
            #     'User-Id': '2a8ff616-6e14-4461-8b4d-2a3fdd019337',
            #     'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VybmFtZTo4NjE3NjEyMzA1NzE2IiwidGVuYW50SWQiOjYyODIsImlzcyI6ImRlZmF1bHQiLCJ0ZW5hbnRBbGlhcyI6ImFnOTM2Mjgya3pxZW0iLCJleHAiOjE2OTI3ODA2NjIwMjIsInVzZXJJZCI6IjJhOGZmNjE2LTZlMTQtNDQ2MS04YjRkLTJhM2ZkZDAxOTMzNyIsInByb2plY3RJZCI6ImRlZmF1bHQiLCJpYXQiOjE2OTE1NzEwNjIwMjJ9.KXY0ZsuTCYBiGv4vaz1gEwlJEMHo_E8Y8WDP7Sf2gTo',
            #     'Content-Type': 'application/json'
            # }
            # logger.info(job["jobStatus"])
            # body = {
            #          # "tagIds": [
            #          #      job["jobStatus"]
            #          # ],
            #          "spaceId": tip_config["spaceId"],
            #          "name": job["jobTitle"],
            #          # "ordered": 0,
            #          # "description": "描述",
            #          # "startTime": "2023-08-09T11:55:01.604Z",
            #          # "timeoutTime": "2023-08-09T11:55:01.604Z",
            #          # "title": std_list[0]["name"],
            #          # "channelId": quote(_gle_user_config["account"]),
            #          "projectPayload": {
            #               "entityType": "job",
            #               "openId": "gllue-jobSubMission-143548",
            #               "tenantId": "ag936282kzqem"
            #          }
            #     }
            # res = requests.post(f"http://mesoor-space.nadileaf.com/v3/channels?channelId={tip_channel_id}",headers=headers,json=body)
            # print(res.status_code)
            # print(res.text)

            # todo channel写入TIP并创建关系

        #     if job_sub_mission_app:
        #         job_sub_mission_task_list: Task = await job_sub_mission_app.sync_job_submission_by_job_order_id(job["id"], schema_config["jobSubMission".lower()])
        #         for job_sub_mis_task in asyncio.as_completed(job_sub_mission_task_list):
        #             print(job_sub_mis_task)
        #             break
        # break


if __name__ == '__main__':
    asyncio.run(gle_sync_executor())