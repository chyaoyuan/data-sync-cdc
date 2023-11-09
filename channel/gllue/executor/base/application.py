import asyncio
import base64
import copy
import json
import uuid
from typing import Optional
import aiofiles
import jmespath

from channel.gllue.executor.base.model import MesoorExtraInUsedConfig
from channel.gllue.executor.config.settings import Settings
from channel.gllue.pull.application.applicaiton import GlePullApplication
from channel.gllue.pull.application.model.sync_model import BaseSyncConfig
from utils.logger import logger
from channel.gllue.executor.model import TipConfig, SyncConfig, StorageToTipConfig
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
        self.tip_app = TipMidApplication(Settings.tip_app_config)

        self.tenant_alias = self.tip_config.tenantAlias

    async def put_to_tip(self,
                         entity_list: list,
                         storage_to_tip_config: StorageToTipConfig,
                         gle_entity_name: str):
        # 因为有多个endpoint所以不在这里指定实体类型
        for entity in entity_list:
            entity["mesoorExtraSourceEntityType"] = gle_entity_name
            entity["mesoorExtraTenantAlias"] = self.tip_config.tenantAlias
        # 先把附件bytes去掉再请求转换
        entity_list_copy = entity_list
        for entity_copy in entity_list_copy:
            self.gle_pull_app.clientcontract_app.pop_entity_file_content(entity_copy)

        converted_entity_list, _ = await self.tip_app.convert_app.convert_batch(
            storage_to_tip_config.convertId, entity_list_copy, self.tip_config.tenantAlias, self.x_source)

        for converted_entity, entity_copy in zip(converted_entity_list, entity_list_copy):
            file_info_list = self.gle_pull_app.base_entity_in_used.get_entity_file_content(entity_copy)
            converted_entity["rawData"] = {}
            converted_entity["rawData"]["content"] = entity_copy
            converted_entity["rawData"]["files"] = [{"fileName": i['fileName'], 'key':f"/{self.tip_config.tenantAlias}/gllue-{i['id']}"}for i in file_info_list]
            converted_entity["standardFields"]["source"] = self.source
            mesoor_extra_in_used_config = converted_entity["customFields"].pop("mesoorExtraInUsedConfig")
            config = MesoorExtraInUsedConfig(**mesoor_extra_in_used_config)
            if "prod-mesoor-space" == storage_to_tip_config.storageToTipService:
                info = converted_entity if not storage_to_tip_config.jmeSPath else \
                    jmespath.search(storage_to_tip_config.jmeSPath, converted_entity)
                if info:
                    await self.tip_app.tip_space_app.upsert_note(
                        storage_to_tip_config.tipEntityName,
                        config.urlPath.openId,
                        info, self.tip_config.tenantAlias)
                    pass
            elif "rule" in storage_to_tip_config.storageToTipService:

                if need_put_status := config.putStatus:
                    _, _status = await self.tip_app.transmitter_app.get(self.tip_config.tenantAlias, storage_to_tip_config.tipEntityName, config.urlPath.openId)
                    if need_put_status != _status:
                        continue
                _, status = await self.tip_app.transmitter_app.put(
                    self.tip_config.tenantAlias,
                    storage_to_tip_config.tipEntityName,
                    config.urlPath.openId,
                    self.x_source,
                    self.x_editor,
                    converted_entity, config.headers)
                # with open(f"{self.tip_config.tenantAlias}_{gle_entity_name}_error.jsonl", "a") as f:
                #     f.write(
                #         json.dumps(
                #             {"request": _, "status": status} ,ensure_ascii=False)+"\n")

    async def upload_file(self, entity_list):
        for entity_copy in entity_list:
            attachment_list = self.gle_pull_app.base_entity_in_used.get_entity_file_content(entity_copy)
            for attachment in attachment_list:
                await asyncio.create_task(self.tip_app.tip_derivation_app.save_b64_file({
                    "fileContent": base64.b64encode(attachment["fileContent"].read()).decode(),
                    "fileName": attachment['fileName'],
                    "key": f"/{self.tip_config.tenantAlias}/gllue-{attachment['id']}"
                }))

    async def execute(self):

        # 主实体同步器
        primary_entity_app = self.gle_pull_app.get_app(self.sync_config.entityName)
        # 主实体fields和映射
        if not self.sync_config.onlyFields:
            field_name_list: str = await primary_entity_app.initialize_field(self.sync_config.syncAttachment,self.sync_config.fieldList)
        else:
            await primary_entity_app.initialize_field(self.sync_config.syncAttachment, self.sync_config.fieldList)
            field_name_list: str = self.sync_config.onlyFields
        if self.sync_config.extraFieldNameList:
            logger.error(self.sync_config.extraFieldNameList)
            field_name_list = f"{field_name_list},{self.sync_config.extraFieldNameList}"
        # 额外多个实体的fields配置 这里保留重新实例化的app是因为加载schema会生成双向mapping，如果重新实例化就不会生成maping
        extra_entity_field_config = {}
        for _ in self.sync_config.extraEntity:
            # 额外实体都是通过主实体内的额外id同步

            extra_config_app = GlePullApplication(self.gle_user_config, {"syncModel": "IdList"}).get_app(_.entityName)
            extra_entity_field_config[_.entityName] = {}
            if _.onlyFields:
                # 必须执行生成双向mapping
                await extra_config_app.initialize_field(_.syncAttachment, [])
                extra_entity_field_config[_.entityName]["fields"]: str = _.onlyFields
            else:
                extra_entity_field_config[_.entityName]["fields"]: str = await extra_config_app.initialize_field(_.syncAttachment,[])
            extra_entity_field_config[_.entityName]["app"] = extra_config_app
        if self.gle_base_config.syncModel == "IdList" or self.gle_base_config.syncModel == "IdRecent":
            task_list = await primary_entity_app.create_tasks(field_name_list, self.sync_config.syncAttachment, id_list=self.sync_config.idList)
        else:
            task_list = await primary_entity_app.create_tasks(field_name_list, self.sync_config.syncAttachment,  gql=self.sync_config.gql)
        # for index, entity_task in enumerate(asyncio.as_completed(task_list)):
        for index, entity_task in enumerate(task_list):
            entity_list, source_response = await entity_task
            if not entity_list:
                continue
            logger.info(f"获取到主实体->{self.sync_config.entityName}->{index} {[i['id'] for i in entity_list]}")
            await self.upload_file(entity_list)
            await asyncio.gather(*[
                self.put_to_tip(
                    entity_list,
                    config,
                    self.sync_config.entityName,
                ) for config in self.sync_config.storageToTipConfig])

            # storage_to_tip_config = self.sync_config.storageToTipConfig[0]
            # converted_entity_list, _ = atip_app.convert_app.convert_batch(
            #     storage_to_tip_config.convertId, entity_list)
            # await asyncio.gather(*[
            #     self.put_to_tip(
            #         tip_app,
            #         entity_list,
            #         config,
            #         self.sync_config.entityName,
            #     ) for config in self.sync_config.storageToTipConfig])
            # await self.put_node_(tip_app, entity_list)
            # 只取一级关联，否则子子孙孙无穷尽
            # result = source_response.get("result", {})
            # result.pop(self.sync_config.entityName, None)
            # logger.info(f"返回值检索到的实体有->{result.keys()}")
            # for extra_entity_config in self.sync_config.extraEntity:
            #     if (extra_entity_name := extra_entity_config.entityName) in result.keys():
            #         id_list = [str(_['id']) for _ in result.get(extra_entity_name, [])]
            #         if id_list:
            #             logger.info(f"检索到关联实体->{extra_entity_name}->{id_list}")
            #             extra_app = extra_entity_field_config[extra_entity_config.entityName]["app"]
            #             extra_field_name_list: str = extra_entity_field_config[extra_entity_config.entityName]["fields"]
            #             if extra_entity_config.extraFieldNameList:
            #                 extra_field_name_list = f"{extra_field_name_list},{extra_entity_config.extraFieldNameList}"
            #             extra_task_list = await extra_app.create_tasks(extra_field_name_list,extra_entity_config.syncAttachment, id_list)
            #             for extra_entity_task in extra_task_list:
            #                 extra_entity_list, _useless = await extra_entity_task
            #                 if not extra_entity_list:
            #                     continue
            #                 if self.sync_config.storageModel == "Tip":
            #                     await asyncio.gather(*[
            #                         self.put_to_tip(
            #                             tip_app,
            #                             extra_entity_list,
            #                             config,
            #                             extra_entity_config.entityName,
            #                             ) for config in extra_entity_config.storageToTipConfig])


    async def sync(self):
        await self.execute()


