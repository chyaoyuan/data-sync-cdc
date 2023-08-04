import asyncio
from typing import Optional

from loguru import logger

from channel.gllue.pull.application.schema.application import GleSchema
from channel.gllue.pull.application.base.model import BaseResponseModel


class GleJobOrder(GleSchema):
    # 每页最大条数
    total_count: int = 5

    def __init__(self, gle_user_config: dict):
        super().__init__(gle_user_config)
        self.b = []

    async def _get_job_info(self, page: int, field_name_list: str):
        res, status = await self.async_session.get(
            url="https://fsgtest.gllue.net/rest/joborder/simple_list_with_ids",
            gle_config=self.gle_user_config.dict(),
            ssl=False,
            params={"fields": field_name_list,
                    "ordering": "-lastUpdateDate",
                    "paginate_by": self.total_count,
                    'page': page},
            func=self.request_response_callback)
        for job in res["result"]["joborder"]:
            logger.info(f"{job['id']}===={job}")

        return res

    async def get_job_info(self, page: int, field_name_list: str):

        job_list = await self._get_job_info(page, field_name_list)
        logger.info(job_list)
        logger.info(f"获取到第{page}页")

    async def get_max_page(self) -> int:
        field_name_list = await self.get_field_name_list("joborder")
        field_name_list = ",".join(field_name_list)
        info = await self._get_job_info(page=1, field_name_list=field_name_list)
        i = BaseResponseModel(**info)
        logger.info("最大页数{}".format(i.totalpages))
        return i.totalpages

    async def get_candidate_id_by_job_order_id(self, status_list: Optional[list] = None):
        """
        status_list用来确定同步这个职位下什么状态的简历，
        以外服gllue前端为例
        jobsubmission_status_kanban=
        apply 应聘
        longlist 加入项目
        cvsent 简历推荐-全部
        cvsent^non_feedback 简历推荐-未反馈
        cvsent^feedbacked 简历推荐-已反馈
        clientinterview-客户面试-全部
        clientinterview^feedbacked-客户面试-已反馈
        clientinterview^non_feedback 客户面试-未反馈
        offersign-offer-全部
        offersign^feedbacked_pass-offer-已接受
        offersign^feedbacked_reject-offer-已拒绝
        offersign^non_feedback-offer-未反馈
        onboard-入职-全部
        onboard^in_probation-入职-在试用期内
        onboard^out_of_probation-入职-已过试用期
        invoice-业绩分配-全部
        invoice^approvaled-业绩分配-已审批
        invoice^no_approval-业绩分配-未审批
        reject-淘汰
        """
        pass

    async def run(self):
        await self.check_token()
        max_page: int = await self.get_max_page()
        field_name_list = await self.get_field_name_list("Candidate")
        field_name_list.append("tags")
        field_name_list = ",".join(field_name_list)
        await asyncio.gather(
            *[
                self._get_job_info(page=_, field_name_list=field_name_list) for _ in range(1, max_page+1)
            ]
        )
        return self.b


if __name__ == '__main__':
    asyncio.run(GleJobOrder(
        {
            "apiServerHost": "https://fsgtest.gllue.net",
            "aesKey": "824531e8cad2a287",
            "account": "api@fsg.com.cn"
        }
    ).run())