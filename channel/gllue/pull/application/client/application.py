# import asyncio
# import copy
# import json
# from typing import Optional
# from urllib.parse import parse_qs, urlencode
#
# import aiohttp
#
# from channel.gllue.pull.application.attachment.application import GleAttachment
# from channel.gllue.pull.application.base.application import BaseApplication
# from utils.logger import logger
# from channel.gllue.pull.application.base.model import BaseResponseModel
# from channel.gllue.pull.application.schema.application import GleSchema
# from channel.gllue.pull.application.model.sync_model import SyncConfig
# from utils.parse_time_interval import parse_time_interval
# from urllib.parse import urlencode
#
#
# class GlePullClient(BaseApplication):
#     # 每页最大条数
#
#     total_count: int = 100
#     entityType = "client".lower()
#
#     def __init__(self, gle_user_config: dict,x):
#         super().__init__(gle_user_config)
#         # 同步需要的配置，搜索不需要
#         self.sync_config = SyncConfig(**x)
#         self.schema_app = GleSchema(gle_user_config)
#         self.attachment_app = GleAttachment(gle_user_config)
#         self.semaphore = asyncio.Semaphore(48)
#
#     async def ___get_candidate_info(self, page: int,
#                                     field_name_list: str,
#                                     check: bool = False,
#                                     overwrite_gql: Optional[str] = None) -> dict:
#         gql = overwrite_gql if overwrite_gql else self.sync_config.gql
#
#         res, status = await self.async_session.get(
#             url=self.settings.get_entity_url.format(entityType=self.entityType),
#             params={
#                 "fields": field_name_list,
#                 "ordering": self.sync_config.orderBy,
#                 "paginate_by": self.total_count,
#                 'page': page,
#                 'gql': gql},
#             func=self.request_response_callback)
#         self.gle_user_id = res["@odata.user_id"]
#         if check:
#             return res
#         if not res.get("result"):
#             logger.warning(f"查询无结果->{self.entityType}->{gql}")
#             return {}
#         return res
#
#     async def get_client_info(self, page: int, field_name_list: str, check: bool = False, overwrite_gql: Optional[str] = None):
#         async with self.semaphore:
#             response = await self.___get_candidate_info(page, field_name_list, check, overwrite_gql)
#             if check:
#                 return response
#             gql = overwrite_gql if overwrite_gql else self.sync_config.gql
#             ids = gql.replace("id__s=", "").split(",")
#             logger.info(response)
#             if not response:
#                 return [{"id": _id for _id in ids}], {}
#             result = response.get("result", {})
#             # 将外部字段合并
#             child_field_name_list = self.schema_app.get_field_name_list_child_from_field_list(field_name_list.split(","))
#             candidate_list = self.schema_app.merge_fields(result[self.entityType], child_field_name_list, result)
#             for candidate in candidate_list:
#                 attachments = candidate.get("attachments") or None
#                 if attachments and self.sync_config.syncAttachment:
#                     await self.attachment_app.get_attachment(attachments, candidate)
#             # 获取除了本身以外还有哪些实体
#             extra_entity_list = list(
#                 set(list(result.keys())) - set(child_field_name_list) - {self.entityType}
#             )
#             # 对额外实体合并
#             extra_entity_map = {}
#             for extra_entity_name in extra_entity_list:
#                 extra_entity_map[extra_entity_name] = self.schema_app._create_extra_entity_id_map(
#                     result.get(extra_entity_name, []))
#             # 对schema映射字典字段进行合并
#             candidate_id_map = self.schema_app.field_id_map.get(self.entityType, {})
#             # 对系统字段映射字典字段进行合并
#             system_id_map = copy.deepcopy(self.schema_app.field_id_map)
#             system_id_map.pop(self.entityType, None)
#             for candidate in candidate_list:
#                 self.schema_app.mesoor_extra(candidate, system_id_map, list(system_id_map.keys()))
#                 self.schema_app.mesoor_extra(candidate, candidate_id_map, list(candidate_id_map.keys()))
#                 self.schema_app.mesoor_extra(candidate, extra_entity_map, list(extra_entity_map.keys()))
#             return candidate_list, response
#
#     async def get_max_page(self, overwrite_gql: Optional[str] = None) -> int:
#         field_name_list = await self.schema_app.get_field_name_list(self.entityType)
#         field_name_list = ",".join(field_name_list)
#         # field_name_list = "operation,id,is_parent,parent__id,parent__type,contractInfo,candidate_authorization_remind,type,name,__name__,citys,industrys,people_count,past_people_count,job_count,type,note_count,attachment_count,gllueext_bdsource"
#
#         info = await self.get_client_info(page=1, field_name_list=field_name_list, check=True, overwrite_gql=overwrite_gql)
#         i = BaseResponseModel(**info)
#         logger.info(f"账户->{self.gle_user_config.account} 实体类型->{self.entityType} 每页{self.total_count}个 共{i.totalpages}页码 共{i.totalcount}个实体")
#         return i.totalpages
#
#     async def run(self):
#         max_page: int = await self.get_max_page()
#         field_name_list = await self.schema_app.get_field_name_list(self.entityType)
#         field_name_list = ",".join(field_name_list)
#         # field_name_list = "operation,id,is_parent,parent__id,parent__type,contractInfo,candidate_authorization_remind,type,name,__name__,citys,industrys,people_count,past_people_count,job_count,type,note_count,attachment_count,gllueext_bdsource"
#         task_list = [asyncio.create_task(self.get_client_info(page=index, field_name_list=field_name_list)) for index in
#                      range(1, max_page + 1)]
#         return task_list
#
#     async def get_clients_by_gql(self, gql: dict):
#         """
#         通过GQL搜索公司
#         """
#         gql_str = urlencode(gql)
#         max_page: int = await self.get_max_page(gql_str)
#         field_name_list = await self.schema_app.get_field_name_list(self.entityType)
#         field_name_list = ",".join(field_name_list)
#         task_list = [asyncio.create_task(
#             self.get_client_info(page=index, field_name_list=field_name_list, overwrite_gql=gql_str)) for index in
#                      range(1, max_page + 1)]
#         return task_list
#
#     async def create_tasks(self, field_name_list: str):
#         if self.sync_config.syncModel == "Id":
#             id_list = [self.sync_config.idList[i:i + self.total_count] for i in
#                        range(0, len(self.sync_config.idList), self.total_count)]
#             task_list = [
#                 self.get_client_info
#                 (1, field_name_list, overwrite_gql=f"id__s={','.join(_id_l)}")
#                 for _id_l in id_list]
#         else:
#             page_total = await self.get_max_page()
#             task_list = [self.get_client_info(index_page, field_name_list) for index_page in
#                          range(1, page_total + 1)]
#         return task_list
#
#     async def get_client_by_gql(self, gql: dict):
#         client_task_list = await self.get_clients_by_gql(gql)
#         total_client_id = None
#         for client_task in asyncio.as_completed(client_task_list):
#             if total_client_id:
#                 break
#             for client in await client_task:
#                 if client["name"] == gql["company_name__eq"]:
#                     total_client_id = client["id"]
#                     total_client_name = client["name"]
#                     logger.info(f"client Exist name->{total_client_name} id->{total_client_id} info->{client}")
#                     return client
#         logger.info(f"client not Exist name->{gql['keyword']}")
#         return None
#
# if __name__ == '__main__':
#     _gle_user_config = {
#         "apiServerHost": "https://www.cgladvisory.com",
#         "aesKey": "398b5ec714c59be2",
#         "account": "system@wearecgl.com",
#     }
#     b = {
#         "syncAttachment": True,
#         "orderBy": "str",
#         "syncModel": "str",
#         # type__eq=prospect&
#         'gql': "keyword=1106120"
#     }
#
#     async def exe():
#
#         g = GlePullClient(_gle_user_config, b)
#         entity_schema = await g.schema_app.get_field_name_list("client")
#         entity_schema.append("attachments")
#         print(entity_schema)
#         task_list = await g.create_tasks(",".join(entity_schema))
#         for candidate_task in asyncio.as_completed(task_list):
#             entity_list = await candidate_task
#             for entity in entity_list:
#                 # logger.info(entity)
#                 pass
#
#
#     asyncio.run(exe())