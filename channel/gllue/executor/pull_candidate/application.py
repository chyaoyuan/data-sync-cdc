import asyncio
import base64
import copy
import json
import os
from typing import Optional
import chardet
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
        # self.entity_name_list.append(self.sync_config.entityName)

    async def execute(self, file=None, output_path=None):
        async with aiohttp.ClientSession() as session:
            gle_pull_app = GlePullApplication(self.gle_user_config, self.sync_config.dict())

            field_name_list: str = await gle_pull_app.candidate_app.initialize_field(
                self.sync_config.syncAttachment, self.sync_config.fieldList, self.sync_config.childFieldList)
            task_list = await gle_pull_app.candidate_app.create_tasks(field_name_list)
            for candidate_task in asyncio.as_completed(task_list):
                entity_list, source_response = await candidate_task
                for entity in entity_list:
                    logger.info(entity)
                    pass
                    logger.info(f"正在保存->{entity['id']}")
                    if file and output_path:

                        for attachment in entity.get("mesoorExtraAttachments", []):
                            if not os.path.exists(f"/Volumes/Expansion/pull_candidate/attachments/{entity['id']}/{attachment['id']}"):
                                os.makedirs(f"/Volumes/Expansion/pull_candidate/attachments/{entity['id']}/{attachment['id']}")
                                cache = copy.deepcopy(attachment)
                                cache.pop("fileContent")
                                logger.info(cache)
                            attachment['fileName'] = "unknown" if not attachment['fileName'] else attachment['fileName'].replace(" ","")
                            async with aiofiles.open(f"/Volumes/Expansion/pull_candidate/attachments/{entity['id']}/{attachment['id']}/{attachment['fileName']}", 'wb') as file2:
                                file_bytes = base64.b64decode(attachment['fileContent'].encode())
                                await file2.write(file_bytes)
                    logger.info(f"保存成功 ID->{entity['id']}")
                    await file.write(json.dumps(gle_pull_app.candidate_app.pop_entity_file_content(entity), ensure_ascii=False) + "\n")

    async def init_schema(self):
        pass

    async def sync(self):
        if self.sync_config.storageModel == "Local":
            async with aiofiles.open(self.sync_config.fileStoragePath, 'a') as file:
                await self.execute(file, self.sync_config.fileStoragePath)
        else:
            await self.execute()


if __name__ == '__main__':
    # _gle_user_config = {
    #     "apiServerHost": "https://fsgtest.gllue.net",
    #     "aesKey": "824531e8cad2a287",
    #     "account": "api@fsg.com.cn"
    # }
    id_list = [i for i in range(2557621, 2558121)]

    _gle_user_config = {
        "apiServerHost": "https://www.cgladvisory.com",
        "aesKey": "398b5ec714c59be2",
        "account": "system@wearecgl.com",
    }
    base_sync_config = {
        "syncModel": "Id",
        "syncAttachment": False,
    }
    _sync_config = {
        "syncAttachment": False,

        "storageModel": "Local",
        "jsonFileStorageName": "res_20231007.jsonl",
        "FileStoragePath": "res_20231007.jsonl",
        "orderBy": "id",
        "startTime": "2023-08-01 00:00:00",
        "endTime": "2023-09-01 00:00:00",
        "recent": "1",
        "unit": "month",
        "timeFieldName": "dateAdded__day_range",
        "idList": id_list,
        "convertId": "Resume:standard:2023_09_04_03_27_59",
        "fieldList": ["attachments", "tags", "functions", "industrys", "locations",],
        "childFieldList": ["candidateeducation", "candidateexperience", "candidateproject", "candidatelanguage", "candidatequalification"],
    }
    g = GleExeApp(_gle_user_config,_sync_config,{})
    asyncio.run(g.sync())