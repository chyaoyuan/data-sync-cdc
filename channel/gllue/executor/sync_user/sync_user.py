import asyncio
import json
from asyncio import Task
from typing import Optional
from utils.logger import logger

from channel.gllue.executor.model import GleUserConfig, SyncConfig, TipConfig
from channel.gllue.pull.application.applicaiton import GlePullApplication
from channel.gllue.pull.application.jobOrder.application import GleJobOrder
from channel.gllue.pull.application.jobSubMission.application import GleJobSubMissionInfo
from channel.gllue.pull.application.schema.application import GleSchema
from channel.gllue.pull.application.user.application import GleUser
from middleware.external.application import external_application


async def sync_user_exe(gle_user_config: dict, sync_config: dict):
    """
    同步谷露的职位(jobOrder)
    根据配置同步子关联实体[职位下候选人](jobSubMission)
    """
    pull_test = True
    # gle 同步基础
    # 获取所有需要同步的实体名
    sync_config = SyncConfig(**sync_config)
    gle_user_config = GleUserConfig(**gle_user_config)
    entity_name_list: list = [entity.entityName for entity in sync_config.childEntityList]
    entity_name_list.append("user")
    entity_name_list: list = list(set(entity_name_list))
    # 运行应用
    gle_pull_app = GlePullApplication(gle_user_config.dict(), sync_config.dict())
    schema_app: GleSchema = gle_pull_app.schema_app
    gle_user_app: GleUser = gle_pull_app.user_app
    # 获取所有配置实体schema
    schema_config: dict = {entity_name: await schema_app.get_schema(entity_name) for entity_name in entity_name_list}
    new_schema = {}
    for schema_name, schema_info in schema_config.items():
        new_schema[schema_name] = ",".join([field_info["name"]for field_info in schema_info])
    schema_config = new_schema
    logger.info(f"获取到Schema的实体为->{list(schema_config.keys())}")

    # tip->channel
    # 不要url编码否则
    tip_channel_id = gle_user_config.account
    # sync->gle-job
    field_name_list: str = await gle_user_app.initialize_field(sync_config.fieldList,sync_config.childFieldList)
    page_total = await gle_user_app.get_max_page()
    logger.info(f"共{page_total}页 每页最多{gle_user_app.total_count}个{'user'}")
    for index_page in range(1, page_total + 1):
        entity_list = await gle_user_app.get_entity_info(index_page, field_name_list)
        logger.debug(f"第{index_page}页 数量->{len(entity_list)} entity->{gle_user_app.entity} id->{[entity['id'] for entity in entity_list]}")
        for entity in entity_list:

            logger.info(entity)
            pass


