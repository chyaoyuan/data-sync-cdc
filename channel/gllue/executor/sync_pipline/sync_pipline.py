import asyncio
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
    entity_name_list.append("jobSubMission")
    entity_name_list: list = list(set(entity_name_list))
    # 运行应用
    gle_pull_app = GlePullApplication(gle_user_config.dict(), sync_config.dict())
    schema_app: GleSchema = gle_pull_app.schema_app
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
    job_sub_mission_app.sync_entity_by_gql()



