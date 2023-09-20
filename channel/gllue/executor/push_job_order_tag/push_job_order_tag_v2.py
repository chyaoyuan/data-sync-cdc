import asyncio
import os
import re
from asyncio import Task
from typing import Optional
from urllib.parse import urlencode
from urllib.parse import quote
import aiohttp
import jmespath

from channel.gllue.executor.push_job_order_tag.function.application import FunctionApplication
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


async def execute(func_app: FunctionApplication, entity: dict, flow: list, tip_app, gle_update_entity: Optional[dict] = None, index=0):
    if not gle_update_entity:
        gle_update_entity = {}
    task = flow[index]
    if index == 0:
        before_task_result = None
    else:
        before_task_result = flow[index-1]["result"]
    if method := task.get("method"):
        logger.info("#"*30)
        res = None
        logger.info(f"running->{method} ->{task}")
        logger.info(f"before_result->{before_task_result}")
        if method == "extract":
            res = await tip_app.tip_tag_app.extract_flatten({"output_category": task["name"]}, entity, task["jmespath"])
            res = res[0].get("tag")
        elif method == "expand":
            res = await tip_app.tip_tag_app.expand_flatten({"texts": before_task_result, "output_category": task["expandCategory"]})
            res = res[0].get("tag")
        elif method == "func":
            if before_task_result:
                result = f'{flow[index-1]["result"]}'
            else:
                result = f'{flow[index]["result"]}'
            func_name = task["func"]
            res: dict = func_app.map(func_name, result)
        elif method == "create_entity":
            if isinstance(flow[index-1]["result"], dict):
                for field_name, _result in zip(task["gllueFieldName"], flow[index-1]["result"].values()):
                    gle_update_entity.update({field_name: _result})
            elif isinstance(flow[index-1]["result"], (str, int)):
                gle_update_entity.update({task["gllueFieldName"][0]: before_task_result})
                logger.error(gle_update_entity)
            elif isinstance(flow[index-1]["result"], list):
                for field_name, _result in zip(task["gllueFieldName"], flow[index-1]["result"]):
                    gle_update_entity.update({field_name: _result})
            else:
                logger.error("未指定的类型")
        if task.get("end"):
            return gle_update_entity
        if res:
            task["result"] = res
        else:
            raise Exception(f"task_error->{index}")
    return await execute(func_app, entity, flow, tip_app, gle_update_entity, index+1)


async def push_job_order_tag_exec(gle_user_config: GleUserConfig, sync_config: SyncConfig, flows: list):
    """
    同步谷露的职位(jobOrder)
    根据配置同步子关联实体[职位下候选人](jobSubMission)
    """
    async with aiohttp.ClientSession() as session:
        tip_app = TipMidApplication(session, settings)
        pull_test = True
        # gle 同步基础
        # 获取所有需要同步的实体名
        entity_name_list = ["joborder"]
        # 运行应用
        gle_pull_app = GlePullApplication(gle_user_config.dict(), sync_config.dict())
        schema_app: GleSchema = gle_pull_app.schema_app
        await schema_app.initialize_field_map_field("joborder")
        func_app = FunctionApplication(schema_app)
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
                logger.info(job_order["id"])
                logger.info("*"*30)
                new_job_order = {}
                flows = [flows[3]]
                for index, flow in enumerate(flows):
                    logger.info(index)
                    gle_entity = await execute(func_app, job_order, flow, tip_app, {}, index=0)
                    logger.info(f"flow_result->{gle_entity}")
                    if gle_entity:
                        new_job_order = {**new_job_order, **gle_entity}
                res = await gle_push_app.job_order_app.update_job_order_by_id(job_order_id=job_order["id"],
                                                                              overwrite_info=new_job_order)
                break






