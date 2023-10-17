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
from channel.gllue.pull.application.model.sync_model import BaseSyncConfig
from middleware.external.application import external_application
from utils.logger import logger
from channel.gllue.executor.model import TipConfig, SyncConfig
from channel.gllue.executor.utils.split_date_range import split_date_range
from TipMidApp import TipMidApplication


class GleExeApp:
    def __init__(self, gle_user_config: dict, base_sync_config: dict, sync_config: dict,
                 tip_config: Optional[dict] = None):
        self.tip_config: Optional[TipConfig] = TipConfig.transform(tip_config) if tip_config else None
        self.gle_user_config = gle_user_config
        self.gle_base_config = BaseSyncConfig(**base_sync_config)
        self.sync_config = SyncConfig(**sync_config)
        self.source = "谷露"
        # 获取所有需要同步的实体的schema
        self.entity_name_list: list = [extra_entity.entityName for extra_entity in self.sync_config.extraEntity]
        # self.entity_name_list.append(self.sync_config.entityName)

    async def execute(self, file_io=None):
        gle_pull_app = GlePullApplication(self.gle_user_config, self.gle_base_config.dict())
        tip_app = TipMidApplication({"ConvertServerHost": "http://localhost:65492",
                                     "TipTransmitterServerHost": "http://localhost:53740"})
        primary_entity_app = gle_pull_app.get_app(self.sync_config.primaryEntityName)
        field_name_list: str = await primary_entity_app.initialize_field(
            self.sync_config.fieldList)
        task_list = await primary_entity_app.create_tasks(field_name_list)
        for entity_task in asyncio.as_completed(task_list):
            entity_list, source_response = await entity_task
            logger.info(f"获取到实体->{self.sync_config.primaryEntityName}->{[i['id'] for i in entity_list]}")
            for entity in entity_list:
                # 转换结果
                copy_entity = copy.deepcopy(entity)
                converted_entity, _ = await tip_app.convert_app.convert_one(
                    self.sync_config.convertId,
                    gle_pull_app.clientcontract_app.pop_entity_file_content(
                        copy_entity))
                logger.info(f"转换实体成功->{self.sync_config.primaryEntityName}->{entity['id']}")
                converted_entity["source"] = self.source
                converted_entity["attachments"] = []
                for attachment in entity.get("mesoorExtraAttachments", []):
                    converted_entity["attachments"].append(
                        {
                         "fileName": attachment["fileName"],
                         "key": f"gllue-{attachment['id']}_{attachment['fileName']}",
                         "isLink": False,
                         "extension": attachment['ext']
                         }
                    )
                _, __ = await tip_app.transmitter_app.put(self.tip_config.tenantAlias, "Contract", f"gllue-{entity['id']}","gllue","data-sync-cdc",converted_entity)
                logger.info(converted_entity)
                # converted_entity["customFields"]["detectedSourceUrl"] = primary_entity_app.create_source_url()




                # logger.info(self.sync_config.syncAttachment == "Local")
                # gle_pull_app.clientcontract_app.pop_entity_file_content(converted_entity)
                # if self.sync_config.syncAttachment == "Local":
                #     for attachment in entity.get("mesoorExtraAttachments", []):
                #         path = f"{self.sync_config.baseAttachmentFileStoragePath}/{attachment['id']}"
                #         if not os.path.exists(path):
                #             os.makedirs(path)
                #         logger.error(path)
                #         attachment['fileName'] = "unknown" if not attachment['fileName'] else attachment[
                #             'fileName'].replace(" ", "")
                #         async with aiofiles.open(f"{path}/{attachment['fileName']}", 'wb') as file2:
                #             file_bytes = base64.b64decode(attachment['fileContent'].encode())
                #             await file2.write(file_bytes)
                # # logger.info(f"保存成功 ID->{entity['id']}")
                # await file_io.write(
                #     json.dumps(gle_pull_app.clientcontract_app.pop_entity_file_content(entity),
                #                ensure_ascii=False) + "\n")
                # if self.tip_config:
                #     external_application.transmitter_app.save_data()


    async def sync(self):
        if self.sync_config.storageModel == "Local":
            path = f"{self.sync_config.jsonFileStoragePath}/{self.sync_config.jsonFileStorageName}"
            if not os.path.exists(self.sync_config.jsonFileStoragePath):
                os.makedirs(self.sync_config.jsonFileStoragePath)
            async with aiofiles.open(path, 'a') as file_io:
                await self.execute(file_io)
        else:
            await self.execute()
