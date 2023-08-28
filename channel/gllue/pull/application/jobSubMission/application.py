import asyncio
from typing import Optional

from loguru import logger

from channel.gllue.pull.application.schema.application import GleSchema
from channel.gllue.pull.application.base.model import BaseResponseModel


class GleJobSubMissionInfo(GleSchema):
    # 每页最大条数
    total_count: int = 100
    entity = "jobSubMission".lower()

    def __init__(self, gle_user_config: dict):
        super().__init__(gle_user_config)

    async def _get_job_sub_mission_info(self, page: int, field_name_list: str, job_order: str, test:bool=False):
        url = self.settings.get_entity_url.format(apiServerHost=self.gle_user_config.apiServerHost, entityType=self.entity).lower()
        res, status = await self.async_session.get(
            url=url,
            ssl=False,
            params={"fields": field_name_list,
                    "ordering": "-lastUpdateDate",
                    "paginate_by": self.total_count,
                    'page': page,
                    "joborder": job_order,
                 },
            func=self.request_response_callback)
        if res.get("message") or None:
            raise Exception(f"{res}==={status}==={url}")
        if test:
            return res

        return [entity for entity in res["result"][self.entity]]

    async def get_max_page(self, job_order: str, gql: Optional[str] = None) -> int:
        field_name_list = await self.get_field_name_list(self.entity)
        field_name_list = ",".join(field_name_list)
        info = await self._get_job_sub_mission_info(page=1, field_name_list=field_name_list, job_order=job_order, test=True)
        i = BaseResponseModel(**info)
        logger.info("最大页数{}".format(i.totalpages))
        return i.totalpages

    async def sync_job_submission_by_job_order_id(self, job_order_id: str, field_name_list: str):
        # 因为之前同步JobOrder已经测试过token了就不在这里测试了
        max_page: int = await self.get_max_page(job_order_id)
        task_list = [
            asyncio.create_task(
                self._get_job_sub_mission_info(page=_, field_name_list=field_name_list, job_order=job_order_id)
            ) for _ in range(1, max_page+1)
        ]
        return task_list

    async def check_candidate_in_job_order_by_job_order_id(self, job_order_id: str, candidate_id: str,):
        logger.info(candidate_id)
        field_name_list = await self.get_field_name_list(self.entity)
        field_name_list = ",".join(field_name_list)
        job_submission_task_list = await self.sync_job_submission_by_job_order_id(job_order_id, field_name_list)
        for job_submission_list in asyncio.as_completed(job_submission_task_list):
            for job_submission in await job_submission_list:
                logger.info(job_submission)
                if job_submission["candidate"] == candidate_id:
                    logger.info(f"job submission Exist job_order_id->{job_order_id} candidate_id->{candidate_id}")
                    return True
        logger.info(f"job submission not Exist")



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