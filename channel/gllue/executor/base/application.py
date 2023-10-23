import asyncio
import base64
import copy
import json
import os
import uuid
from typing import Optional
import chardet
import aiofiles
import aiohttp

from channel.gllue.pull.application.applicaiton import GlePullApplication
from channel.gllue.pull.application.model.sync_model import BaseSyncConfig
from middleware.external.application import external_application
from utils.logger import logger
from channel.gllue.executor.model import TipConfig, SyncConfig, StorageToTipConfig
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
        self.x_source = "gllue"
        self.x_editor = "data-sync-cdc"
        self.gle_pull_app = GlePullApplication(self.gle_user_config, self.gle_base_config.dict())
        # 获取所有需要同步的实体的schema
        # self.entity_name_list: list = [extra_entity.entityName for extra_entity in self.sync_config.extraEntity]
        # self.entity_name_list.append(self.sync_config.entityName)

    async def put_to_tip(self, tip_app: TipMidApplication,
                         entity_list: list,
                         storage_to_tip_config: StorageToTipConfig,
                         gle_entity_name: str,

):
        # for entity in entity_list:
        #     entity["sourceEntityType"] =
        entity_list_copy: list = copy.deepcopy(entity_list)
        # 先把附件去掉再请求转换，省带宽 加速
        for entity_copy in entity_list_copy:
            attachment_list = self.gle_pull_app.base_entity_in_used.get_entity_file_content(entity_copy)
            for attachment in attachment_list:
                # base64.b64encode(con).decode()
                # with open("xx.pdf", "wb") as f:
                #     f.write(base64.b64decode(attachment["fileContent"].encode()))


                await tip_app.tip_derivation_app.save_file({
                    "fileContent": base64.b64decode(attachment["fileContent"].encode()),
                    "fileName": attachment['fileName'],
                    "key": f"gllue-{attachment['id']}"
                })
        for entity_copy in entity_list_copy:
            self.gle_pull_app.clientcontract_app.pop_entity_file_content(entity_copy)
        converted_entity_list, _ = await tip_app.convert_app.convert_batch(storage_to_tip_config.convertId, entity_list_copy)
        for converted_entity, entity_copy in zip(converted_entity_list, entity_list_copy):
            converted_entity["rawData"] = {}
            converted_entity["rawData"]["content"] = entity_copy
            converted_entity["rawData"]["files"] = self.gle_pull_app.base_entity_in_used.get_entity_file_content(entity_copy)
            converted_entity["standardFields"]["source"] = self.source
            logger.info(storage_to_tip_config.tipEntityName)
            _, status = await tip_app.transmitter_app.put(
                self.tip_config.tenantAlias,
                storage_to_tip_config.tipEntityName,
                f"gllue-{entity_copy['id']}",
                self.x_source,
                self.x_editor,
                converted_entity
                                        )
            if status != 200:
                logger.error(converted_entity)
                logger.error(entity_copy)
        async with aiofiles.open(f"./data/converted-{storage_to_tip_config.tipEntityName}.jsonl","a") as f:
            await asyncio.gather(*[
                f.write(json.dumps(converted_entity, ensure_ascii=False) + "\n") for converted_entity in converted_entity_list
            ])

    async def execute(self):

        tip_app = TipMidApplication({"ConvertServerHost": "http://localhost:65492",
                                     "TipTransmitterServerHost": "http://ruleengine.nadileaf.com",
                                     "StorageDerivationServerHost": "http://localhost:61505"})
        # 主实体同步器
        primary_entity_app = self.gle_pull_app.get_app(self.sync_config.entityName)
        # 主实体fields和映射
        logger.error(self.sync_config.fieldList)
        if not self.sync_config.onlyFields:
            field_name_list: str = await primary_entity_app.initialize_field(self.sync_config.fieldList)
            if self.sync_config.extraFieldNameList:
                field_name_list = f"{field_name_list},{self.sync_config.extraFieldNameList}"
        else:
            # self.sync_config.fieldList
            await primary_entity_app.initialize_field(self.sync_config.fieldList)
            field_name_list: str = self.sync_config.onlyFields
        logger.info(field_name_list.split(","))
        # 额外多个实体的fields配置 这里保留重新实例化的app是因为加载schema会生成双向mapping，如果重新实例化就不会生成maping
        extra_entity_field_config = {}
        for _ in self.sync_config.extraEntity:
            # 额外实体都是通过主实体内的额外id同步

            extra_config_app = GlePullApplication(self.gle_user_config, {"syncModel": "IdList"}).get_app(_.entityName)
            extra_entity_field_config[_.entityName] = {}
            if _.onlyFields:
                # 必须执行生成双向mapping
                await extra_config_app.initialize_field([])
                extra_entity_field_config[_.entityName]["fields"]: str = _.onlyFields
            else:
                extra_entity_field_config[_.entityName]["fields"]: str = await extra_config_app.initialize_field([])
            extra_entity_field_config[_.entityName]["app"] = extra_config_app
        task_list = await primary_entity_app.create_tasks(field_name_list, gql=self.sync_config.gql)
        for entity_task in asyncio.as_completed(task_list):
            entity_list, source_response = await entity_task
            logger.info(f"获取到主实体->{self.sync_config.entityName}->{[i['id'] for i in entity_list]}")

            if self.sync_config.storageModel == "Tip":
                await asyncio.gather(*[
                    self.put_to_tip(
                        tip_app,
                        entity_list,
                        config,
                        self.sync_config.entityName,
                        ) for config in self.sync_config.storageToTipConfig])
                async with aiofiles.open(f"./data/source-{self.sync_config.entityName}.jsonl", "a") as f:
                    await asyncio.gather(*[
                        f.write(json.dumps(self.gle_pull_app.candidate_app.pop_entity_file_content(entity_copy), ensure_ascii=False) + "\n") for entity_copy in entity_list
                    ])

            # 只取一级关联，否则子子孙孙无穷尽
            result = source_response.get("result")
            result.pop(self.sync_config.entityName, None)
            logger.info(f"实体共有->{result.keys()}")
            for extra_entity_config in self.sync_config.extraEntity:
                if (extra_entity_name := extra_entity_config.entityName) in result.keys():
                    id_list = [str(_['id']) for _ in result.get(extra_entity_name, [])]
                    if id_list:
                        logger.info(f"获取到关联实体->{extra_entity_name}->{id_list}")
                        extra_app = extra_entity_field_config[extra_entity_config.entityName]["app"]
                        extra_field_name_list: str = extra_entity_field_config[extra_entity_config.entityName]["fields"]
                        if extra_entity_config.extraFieldNameList:
                            extra_field_name_list = f"{extra_field_name_list},{extra_entity_config.extraFieldNameList}"
                        extra_task_list = await extra_app.create_tasks(extra_field_name_list, id_list)
                        for extra_entity_task in asyncio.as_completed(extra_task_list):
                            extra_entity_list, _useless = await extra_entity_task
                            if self.sync_config.storageModel == "Tip":
                                await asyncio.gather(*[
                                    self.put_to_tip(
                                        tip_app,
                                        extra_entity_list,
                                        config,
                                        self.sync_config.entityName,
                                        ) for config in extra_entity_config.storageToTipConfig])
                                async with aiofiles.open(f"./data/source-{extra_entity_config.entityName}.jsonl", "a") as f:
                                    await asyncio.gather(*[
                                        f.write(
                                            json.dumps(self.gle_pull_app.candidate_app.pop_entity_file_content(extra_entity),
                                                       ensure_ascii=False) + "\n") for extra_entity in extra_entity_list
                                    ])



            quit()

    async def sync(self):
        await self.execute()


