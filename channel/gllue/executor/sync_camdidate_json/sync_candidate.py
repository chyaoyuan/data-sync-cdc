import asyncio
import time
import jmespath
import requests
from loguru import logger
from channel.gllue.pull.application.model.sync_model import SyncConfig
from channel.gllue.pull.application.applicaiton import GlePullApplication
from channel.gllue.executor.config import gllue_industry_config_map, gllue_zhienng_config_map
from channel.gllue.push.application.application import GlePushApplication
from middleware.application import mid
# 如果解析结果没有则使用原值的字段

# 如果只有此字段则不推送
_if_only_exist = ["id"]


def get_gle_func_id(func_name_list: list):
    res = []
    for industry in func_name_list:
        gllue_industry_id = gllue_zhienng_config_map.get(industry)
        if gllue_industry_id:
            res.append(str(gllue_industry_id))
    return ",".join(res)


def get_gle_industry_id(industry_name_list: list):
    res = []
    print(industry_name_list)
    for industry in industry_name_list:
        gllue_industry_id = gllue_industry_config_map.get(industry)
        if gllue_industry_id:
            res.append(str(gllue_industry_id))
    return ",".join(res)


def create_need_remove_key_list(if_exist_not_push_list: list, data: dict):
    need_remove_key_list = []
    for jmespath_grama in if_exist_not_push_list:
        verify = jmespath.search(jmespath_grama, data)
        if verify:
            need_remove_key_list.append(jmespath_grama)
    return need_remove_key_list


def remove_key(need_remove_key_list: list, data: dict):
    for key in need_remove_key_list:
        data.pop(key)


def only_key_check(_if_only_exist: list, data: dict):
    data_key_list = data.keys()
    for data_key in data_key_list:
        if data_key not in _if_only_exist:
            return False
    return True


async def sync_candidate_pull_and_push(gle_user_config: dict, sync_config: dict):
    candidate_pull_app = GlePullApplication(gle_user_config, sync_config).candidate_app
    await candidate_pull_app.check_token()
    sync_config = SyncConfig(**sync_config)
    field_name_list: str = await candidate_pull_app.initialize_field(sync_config.fieldList, sync_config.childFieldList)
    page_total = await candidate_pull_app.get_max_page()
    logger.info(f"共{page_total}页 每页最多{candidate_pull_app.total_count}个候选人")
    for index_page in range(1, page_total + 1):
        entity_list = await candidate_pull_app.get_candidate_info(index_page, field_name_list)
        logger.debug(f"第{index_page}页 数量->{len(entity_list)} entity->{candidate_pull_app.entity} id->{[entity['id'] for entity in entity_list]}")
        for entity in entity_list:
            logger.info(entity)




