# import asyncio
# import base64
# import copy
# import json
# import uuid
# from typing import Optional
# import aiofiles
# import jmespath
#
# from channel.gllue.executor.base.model import MesoorExtraInUsedConfig
# from channel.gllue.executor.config.settings import Settings
# from channel.gllue.pull.application.applicaiton import GlePullApplication
# from channel.gllue.pull.application.model.sync_model import BaseSyncConfig
# from utils.logger import logger
# from channel.gllue.executor.model import TipConfig, SyncConfig, StorageToTipConfig
# from TipMidApp import TipMidApplication
#
#
# class GleExeApp:
#     def __init__(self, gle_user_config: dict, base_sync_config: dict, sync_config: dict,
#                  tip_config: Optional[dict] = None):
#         self.tip_config: Optional[TipConfig] = TipConfig.transform(tip_config) if tip_config else None
#         self.gle_user_config = gle_user_config
#         self.gle_base_config = BaseSyncConfig(**base_sync_config)
#         self.sync_config = SyncConfig(**sync_config)
#         self.source = "谷露"
#         self.x_source = "gllue"
#         self.x_editor = "data-sync-cdc"
#         self.gle_pull_app = GlePullApplication(self.gle_user_config, self.gle_base_config.dict())
#         self.tip_app = TipMidApplication(Settings.tip_app_config)
#
#     async def put_to_tip(self,
#                          entity_list: list,
#                          storage_to_tip_config: StorageToTipConfig,
#                          gle_entity_name: str):
#         # 因为有多个endpoint所以不在这里指定实体类型
#         for entity in entity_list:
#             entity["mesoorExtraSourceEntityType"] = gle_entity_name
#             entity["mesoorExtraTenantAlias"] = self.tip_config.tenantAlias
#         entity_list_copy: list = copy.deepcopy(entity_list)
#         # 递归查询符合附件格式的json并抽取出来gather保存
#         for entity_copy in entity_list_copy:
#             attachment_list = self.gle_pull_app.base_entity_in_used.get_entity_file_content(entity_copy)
#             for attachment in attachment_list:
#                 # await self.tip_app.tip_derivation_app.save_file({
#                 #     "fileContent": base64.b64decode(attachment["fileContent"].encode()),
#                 #     "fileName": attachment['fileName'],
#                 #     "key": f"gllue-{attachment['id']}"
#                 # })
#                 await self.tip_app.tip_derivation_app.save_b64_file({
#                     "fileContent": base64.b64encode(attachment["fileContent"]).decode(),
#                     "fileName": attachment['fileName'],
#                     "key": f"/{self.tip_config.tenantAlias}/gllue-{attachment['id']}"
#                 })
#             if attachment_list:
#                 logger.info(f"attachment_upload_success-谷露实体->{gle_entity_name}"
#                             f" id->{entity_copy['id']} id->{[i['id'] for i in attachment_list]}")
#         # 先把附件去掉再请求转换，省带宽 加速
#         for entity_copy in entity_list_copy:
#             self.gle_pull_app.clientcontract_app.pop_entity_file_content(entity_copy)
#         converted_entity_list, _ = await self.tip_app.convert_app.convert_batch(
#             storage_to_tip_config.convertId, entity_list_copy, self.tip_config.tenantAlias, self.x_source)
#
#         for converted_entity, entity_copy in zip(converted_entity_list, entity_list_copy):
#             logger.info(entity_copy['id'])
#             file_info_list = self.gle_pull_app.base_entity_in_used.get_entity_file_content(entity_copy)
#             converted_entity["rawData"] = {}
#             # converted_entity["rawData"]["content"] = entity_copy
#             converted_entity["rawData"]["files"] = [{"fileName": i['fileName'],'key':f"/{self.tip_config.tenantAlias}/gllue-{i['id']}"}for i in file_info_list]
#             converted_entity["standardFields"]["source"] = self.source
#             mesoor_extra_in_used_config = converted_entity["customFields"].pop("mesoorExtraInUsedConfig")
#             config = MesoorExtraInUsedConfig(**mesoor_extra_in_used_config)
#             if "prod-mesoor-space" == storage_to_tip_config.storageToTipService:
#                 info = converted_entity if not storage_to_tip_config.jmeSPath else \
#                     jmespath.search(storage_to_tip_config.jmeSPath, converted_entity)
#                 if info:
#                     await self.tip_app.tip_space_app.upsert_note(
#                         storage_to_tip_config.tipEntityName,
#                         config.urlPath.openId,
#                         info, self.tip_config.tenantAlias)
#                     pass
#             elif "rule" in storage_to_tip_config.storageToTipService:
#
#                 if need_put_status := config.putStatus:
#                     _, _status = await self.tip_app.transmitter_app.get(self.tip_config.tenantAlias, storage_to_tip_config.tipEntityName, config.urlPath.openId)
#                     if need_put_status != _status:
#                         continue
#                 _, status = await self.tip_app.transmitter_app.put(
#                     self.tip_config.tenantAlias,
#                     storage_to_tip_config.tipEntityName,
#                     config.urlPath.openId,
#                     self.x_source,
#                     self.x_editor,
#                     converted_entity, config.headers)
#                 if status != 200:
#                     async with aiofiles.open(f"./data/error_entity_{storage_to_tip_config.tipEntityName}.jsonl","w") as f:
#                         await f.write(
#                             json.dumps({"message": _,"source":entity_copy,"std":converted_entity})
#                         )
#                     logger.error(converted_entity)
#                     logger.error(entity_copy)
#
#
#         # async with aiofiles.open(f"./data/converted-{storage_to_tip_config.tipEntityName}.jsonl", "a") as f:
#         #     await asyncio.gather(*[
#         #         f.write(json.dumps(converted_entity, ensure_ascii=False) + "\n") for converted_entity in converted_entity_list
#         #     ])
#
#     async def execute(self):
#         async with aiofiles.open(
#                 "/Users/chenjiabin/Documents/data.jsonl") as f:
#             index = 0
#             while line := f.readline():
#                 line = await line
#                 entity_list = json.loads(line)
#                 if index < 2180:
#                     index = index + 1
#                     continue
#
#                 for config in self.sync_config.storageToTipConfig:
#                     await self.put_to_tip(
#                             entity_list,
#                             config,
#                             self.sync_config.entityName,
#                         )
#                 print(f"success->{index}")
#                 index = index + 1
#
#     async def sync(self):
#         await self.execute()
#
#
