import asyncio
from typing import Optional

from channel.gllue.pull.application.attachment.application import GleAttachment
from channel.gllue.pull.application.entity.application import GleEntityApplication
from utils.logger import logger

from channel.gllue.pull.application.model.sync_model import SyncConfig, BaseSyncConfig
from channel.gllue.pull.application.schema.application import GleSchema
from channel.gllue.pull.application.base.model import BaseResponseModel


class GleJobSubMissionInfo(GleEntityApplication):
    add_field_list = []
    # add_field_list = ["attachments", "tags", "functions", "industrys", "locations"]
    entityType: str = "jobSubMission".lower()
    # 每页最大条数
    total_count: int = 100
    # 每个请求延迟N秒
    sleep_time = 0
    # 最大并发数
    concurrency_level = 20

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



if __name__ == '__main__':
    asyncio.run(GleJobSubMissionInfo(
        {
            "apiServerHost": "https://www.cgladvisory.com",
            "aesKey": "eae48bfe137cc656",
            "account": "system@wearecgl.com"
        }
    ).sync_job_submission_by_job_order_id())



    # async def get_candidate_id_by_job_order_id(self, status_list: Optional[list] = None):
    #     """
    #     status_list用来确定同步这个职位下什么状态的简历，
    #     以外服gllue前端为例
    #     jobsubmission_status_kanban=
    #     apply 应聘
    #     longlist 加入项目
    #     cvsent 简历推荐-全部
    #     cvsent^non_feedback 简历推荐-未反馈
    #     cvsent^feedbacked 简历推荐-已反馈
    #     clientinterview-客户面试-全部
    #     clientinterview^feedbacked-客户面试-已反馈
    #     clientinterview^non_feedback 客户面试-未反馈
    #     offersign-offer-全部
    #     offersign^feedbacked_pass-offer-已接受
    #     offersign^feedbacked_reject-offer-已拒绝
    #     offersign^non_feedback-offer-未反馈
    #     onboard-入职-全部
    #     onboard^in_probation-入职-在试用期内
    #     onboard^out_of_probation-入职-已过试用期
    #     invoice-业绩分配-全部
    #     invoice^approvaled-业绩分配-已审批
    #     invoice^no_approval-业绩分配-未审批
    #     reject-淘汰
    #     """
    #     pass