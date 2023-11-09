import copy
from typing import Optional

from channel.gllue.pull.application.attachment.application import GleAttachment
from channel.gllue.pull.application.entity.application import GleEntityApplication
from utils.logger import logger

from channel.gllue.pull.application.model.sync_model import BaseSyncConfig
from channel.gllue.pull.application.schema.application import GleSchema


class GleJobSubMissionInfo(GleEntityApplication):
    entityType: str = "jobSubMission".lower()

    def __init__(self, gle_user_config: dict, base_sync_config: dict):
        super().__init__(gle_user_config, base_sync_config)
        self.base_sync_config = BaseSyncConfig(**base_sync_config)
        self.schema_config = {}
        self.candidate_function_map = {}
        # schema
        self.schema_app = GleSchema(gle_user_config)
        # 附件
        self.attachment_app = GleAttachment(gle_user_config)
        # 用户/操作者
        self.gle_user_id: Optional[int] = None

    @staticmethod
    def get_info_from_list(_id, entity_list):
        for entity in entity_list:
            if entity['id'] == _id:
                return entity
        raise Exception()


    async def get_entity_info(self, limit, page: int, sync_attachment: bool, field_name_list: str, gql: str, check: bool = False):
        # async with limit:
        response = await self._get_entity_info(page, field_name_list, check, gql)
        if not response:
            return [], {}
        result = response.get("result", {})
        # 将外部字段合并
        child_field_name_list = self.schema_app.get_field_name_list_child_from_field_list(field_name_list.split(","))
        entity_list = self.schema_app.merge_fields(self.entityType, result[self.entityType], child_field_name_list,result)

        for entity in entity_list:
            attachments = entity.get("attachments") or None
            if attachments and sync_attachment:
                attachments_ids = await self.attachment_app.get_attachment(attachments, entity)
                logger.info(f"get_attachment_success: type->{self.entityType} {entity['id']} attachments_ids->{attachments_ids}")
        # 获取除了本身以外还有哪些实体
        extra_entity_list = list(
            set(list(result.keys())) - set(child_field_name_list) - {self.entityType}
        )
        # 对额外实体合并
        extra_entity_map = {}
        for extra_entity_name in extra_entity_list:
            extra_entity_map[extra_entity_name] = self.schema_app._create_extra_entity_id_map(
                result.get(extra_entity_name, []))
        # 对schema映射字典字段进行合并
        entity_id_map = self.schema_app.field_id_map.get(self.entityType, {})
        # 对系统字段映射字典字段进行合并
        system_id_map = copy.deepcopy(self.schema_app.field_id_map)
        system_id_map.pop(self.entityType, None)
        for entity in entity_list:
            self.schema_app.mesoor_extra(entity, system_id_map, list(system_id_map.keys()))
            self.schema_app.mesoor_extra(entity, entity_id_map, list(entity_id_map.keys()))
            self.schema_app.mesoor_extra(entity, extra_entity_map, list(extra_entity_map.keys()))
        un_repeat_set = set()
        # 有的配置会导致生成两个相同实体，第一个信息全第二个不全，这里把它去重
        new_entity_list = []
        for entity in entity_list:
            _id = entity["id"]
            if _id not in un_repeat_set:
                new_entity_list.append(entity)
                un_repeat_set.add(_id)
        # 这段代码是特殊给jobsubmission加的，转换做不到只能我这里转
        for entity in entity_list:
            mesoor_extra_pipeline = []
            for k in entity.keys():
                if "_set" in k and (entity[k] or None) and k not in ["note_set"]:
                    name = k.replace("_set", "")
                    ids = entity.get(k, [])
                    for _id in ids:
                        info = copy.deepcopy(self.get_info_from_list(_id, result.get(name)))
                        info["mesoorExtraStage"] = name
                        mesoor_extra_pipeline.append(info)
            entity["mesoorExtraPipeline"] = mesoor_extra_pipeline
        return new_entity_list, response

    # async def sync_job_submission_by_job_order_id(self, job_order_id: str, field_name_list: str):
    #     """
    #     根据JobOrderId查找JobSubMission
    #     """
    #     # 因为之前同步JobOrder已经测试过token了就不在这里测试了
    #     overwrite_gql = f"joborder={job_order_id}"
    #     max_page: int = await self.get_max_page(overwrite_gql=overwrite_gql)
    #     logger.info(max_page)
    #     task_list = [
    #         asyncio.create_task(
    #             self._get_job_sub_mission_info(page=_, field_name_list=field_name_list, test=False, overwrite_gql=overwrite_gql)
    #         ) for _ in range(1, max_page+1)
    #     ]
    #     return task_list
    #
    # async def check_candidate_in_job_order_by_job_order_id(self, job_order_id: str, candidate_id: str,):
    #     """
    #     通过CandidateId、JobOrderId查看是否绑定为JobSubMission
    #     """
    #     field_name_list = await self.get_field_name_list(self.entity)
    #     field_name_list = ",".join(field_name_list)
    #     job_submission_task_list = await self.sync_job_submission_by_job_order_id(job_order_id, field_name_list)
    #     for job_submission_list in asyncio.as_completed(job_submission_task_list):
    #         for job_submission in await job_submission_list:
    #             logger.info(job_submission)
    #             if job_submission["candidate"] == candidate_id:
    #                 logger.info(f"job submission Exist job_order_id->{job_order_id} candidate_id->{candidate_id}")
    #                 return True
    #     logger.info(f"job submission not Exist")
    #
    # async def _sync(self):
    #     field_name_list = await self.get_field_name_list(self.entity)
    #     a = "operation,mark,candidate__chineseName,candidate__islimited,candidate__id,id,candidate__attachment_count,candidate__joborder,candidate__note_count,candidate__englishName,candidate__chineseName,candidate__islimited,candidate__js_is_locked,candidate__locked_joborder____name__,candidate__js_lock_user____name__,candidate__js_lock_time,candidate__type,candidate__jobsubmission_count_withaccess,glluemeuser_info,is_read,portalresume_created_new_candidate,channel__code,candidate__jobsubmission_lock_type,candidate__dupalert_info,candidate__is_hide,candidate__hide_level,candidate__hider____name__,candidate__hide_time,candidate__same_name_candidate_info,candidate__contractInfo,candidate__name,candidate__company__type,candidate__company__is_parent,candidate__company__parent,candidate__company__parent__id,candidate__company__parent__type,candidate__company,candidate__title,joborder__client__name,joborder__client__candidate_authorization_remind,joborder__islimited,joborder__jobTitle,glluemeuser_info,glluemeuser__type,portalapply__portalposition__record_type,candidate__id,candidate__chineseName,candidate__islimited,joborder__id,detail,lastUpdateDate,candidate__gllueextClient_report_comments,presenttoconsultant_set__user____name__,presenttoconsultant_set__user,cvsent_set__date,clientinterview_set__dateAdded,clientinterview_set__date,mark".split(",")
    #     field_name_list = ",".join(list(set(field_name_list+a)))
    #     max_page: int = await self.get_max_page()
    #     task_list = [
    #         asyncio.create_task(
    #             self._get_job_sub_mission_info(page=_, field_name_list=field_name_list)
    #         ) for _ in range(1, max_page + 1)
    #     ]
    #     return task_list
    #
    # async def sync(self):
    #     task_list = await self._sync()

