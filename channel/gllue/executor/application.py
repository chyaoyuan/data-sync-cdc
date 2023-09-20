import json
from typing import Optional

import aiofiles
import aiohttp

from channel.gllue.pull.application.applicaiton import GlePullApplication
from utils.logger import logger
from channel.gllue.executor.model import TipConfig, SyncConfig
from channel.gllue.executor.utils.split_date_range import split_date_range


class GleExeApp:
    def __init__(self, gle_user_config: dict, sync_config: dict, tip_config: Optional[dict] = None):
        self.tip_config: Optional[TipConfig] = TipConfig.transform(tip_config) if tip_config else None
        self.gle_user_config = gle_user_config
        self.sync_config = SyncConfig(**sync_config)
        self.source = "谷露"
        # 获取所有需要同步的实体的schema
        self.entity_name_list: list = [extra_entity.entityName for extra_entity in self.sync_config.extraEntity]
        self.entity_name_list.append(self.sync_config.entityName)
    # def map_sync_config(self):
    #     """因为每个筛选条件上限为1W个，所以这里会sync_config的时间段把时间分成每天,尽量保证每段配置获取的实体小于1W"""
    #     if (start_time := self.sync_config["startTime"]) and (end_time := self.sync_config["endTime"]) and (start_time != end_time):
    #         time_list = split_date_range(start_time, end_time)
    #         config_list = [{**self.sync_config, **i} for i in time_list]
    #     else:
    #         config_list = [self.sync_config]
    #     logger.info(f"创建了->{len(config_list)}条配置")
    #     return config_list

    async def execute(self, file=None):
        async with aiohttp.ClientSession() as session:
            convert_app = ConvertApp(session, {"ConvertServerHost": "http://converter.nadileaf.com"})
            gle_pull_app = GlePullApplication(self.gle_user_config, self.sync_config.dict())

            field_name_list: str = await candidate_pull_app.initialize_field(self.sync_config.fieldList,
                                                                             self.sync_config.childFieldList)
            task_list = await candidate_pull_app.create_tasks(field_name_list)
            for candidate_task in asyncio.as_completed(task_list):
                entity_list, source_response = await candidate_task
                for entity in entity_list:
                    logger.info(entity["id"])
                    if file:
                        logger.info(f"写入ID->{entity['id']}")
                        await file.write(json.dumps(entity, ensure_ascii=False) + "\n")
    async def init_schema(self):


    async def sync(self):
        if self.sync_config.storageModel == "Local":
            async with aiofiles.open(self.sync_config.fileStoragePath, 'a') as file:
                await self.execute(file)
        else:
            await self.execute()


if __name__ == '__main__':
    # _gle_user_config = {
    #     "apiServerHost": "https://fsgtest.gllue.net",
    #     "aesKey": "824531e8cad2a287",
    #     "account": "api@fsg.com.cn"
    # }
    _gle_user_config = {
        "apiServerHost": "https://www.cgladvisory.com",
        "aesKey": "398b5ec714c59be2",
        "account": "system@wearecgl.com",
    }
    _sync_config = {
        "syncAttachment": False,
        "syncModel": "Id",
        "storageModel": "Local",
        "fileStoragePath": "old_res.jsonl",
        "orderBy": "id",
        "recent": "50",
        "unit": "year",
        "timeFieldName": "dateAdded__day_range",
        "idList": [],
        "convertId": "Resume:standard:2023_09_04_03_27_59",
        "fieldList": ["attachments", "tags", "functions", "industrys", "locations",
                      "candidateexperience_set__client__name"],
        "childFieldList": ["candidateeducation", "candidateexperience", "candidateproject", "candidatelanguage", "candidatequalification"],
        "extraEntity": [
            {"entityType": "jobsubmission", "convertId": "convertId"},
            {"entityType": "client", "convertId": "convertId"},
            {"entityType": "joborder", "convertId": "convertId"}]
    }
    g = GleExeApp(_gle_user_config,_sync_config,{})