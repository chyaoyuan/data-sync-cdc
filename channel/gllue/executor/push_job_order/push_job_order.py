import asyncio
from asyncio import Task
from typing import Optional
from urllib.parse import urlencode
from urllib.parse import quote
import requests
from utils.logger import logger
import jmespath
from channel.gllue.executor.model import GleUserConfig, SyncConfig, TipConfig
from channel.gllue.pull.application.applicaiton import GlePullApplication
from channel.gllue.pull.application.client.application import GlePullClient
from channel.gllue.pull.application.jobOrder.application import GleJobOrder
from channel.gllue.pull.application.jobSubMission.application import GleJobSubMissionInfo
from channel.gllue.pull.application.schema.application import GleSchema
from channel.gllue.push.application.application import GlePushApplication
from middleware.external.application import external_application
from middleware.storage.application import tip_space_application


async def push_gle_job_order_executor(gle_user_config: GleUserConfig,
                                      sync_config: SyncConfig,
                                      tip_business_partner: dict,
                                      tip_job: dict,
                                      tip_resume: dict,
                                      job_order: Optional[dict] = None,
                                      client: Optional[dict] = None,
                                      candidate: Optional[dict] = None):
    """
    同步谷露的职位(jobOrder)
    根据配置同步子关联实体[职位下候选人](jobSubMission)
    """

    # Job
    tip_client_name = jmespath.search("data.standardFields.name", tip_business_partner)
    tip_project_name = jmespath.search("data.standardFields.name", tip_job)
    tip_candidate_name = jmespath.search("data.standardFields.humanInfo.name", tip_resume)
    tip_email = jmespath.search("data.standardFields.contactInfo.personalEmail", tip_resume)
    tip_phone = jmespath.search("data.standardFields.contactInfo.mobilePhoneNumber", tip_resume)
    logger.info(f"客户名称->{tip_client_name}")
    logger.info(f"项目名称->{tip_project_name}")
    logger.info(f"候选人名称->{tip_candidate_name}")
    logger.info(f"候选人邮箱->{tip_email}")
    logger.info(f"候选人手机号{tip_phone}")
    # 运行应用
    gle_pull_app = GlePullApplication(gle_user_config.dict(), sync_config.dict())
    gle_push_app = GlePushApplication(gle_user_config.dict())
    client_app: GlePullClient = gle_pull_app.client_app
    job_order_app = gle_pull_app.job_order_app
    # 查询    公司名称->公司Info
    client_info = await client_app.get_client_by_gql({"company_name__eq": tip_client_name})
    logger.info(client_info)
    # 查不到  公司名称 则新建
    if not client_info:
        client_info = await gle_push_app.client_app.put_client(tip_client_name, client)
        logger.info(client_info)
    # 查询 公司ID+项目名->项目Info（因为谷露可以创建同名项目只取最新的）
    job_order_info = await job_order_app.get_job_order_by_gql({"jobTitle__eq": tip_project_name, "client__s": client_info["id"]})
    logger.info(job_order_info)
    if not job_order_info:
        job_order_info = await gle_push_app.job_order_app.put_job_order(tip_project_name, client_info["id"], job_order)
    # 查询候选人是否存在
    candidate_info = await gle_pull_app.candidate_app.get_candidate_by_contact_gql({"mobile": tip_phone, "email": tip_email})
    logger.info(candidate_info)
    if candidate_info:
        if not await gle_pull_app.job_sub_mission_app.check_candidate_in_job_order_by_job_order_id(job_order_info["id"],candidate_info["id"]):
            await gle_push_app.job_order_app.put_candidate_under_job_order_by_candidate_id(job_order_info["id"], candidate_list=[candidate_info["id"]])
            logger.info(f"候选人已存在但未关联 client_id->{client_info['id']} job_id->{job_order_info['id']} candidate_id->{candidate_info['id']} 执行移动候选人到项目下操作")
        else:
            logger.info(f"候选人已存在已关联 client_id->{client_info['id']} job_id->{job_order_info['id']} candidate_id->{candidate_info['id']}")
        await gle_push_app.candidate_app.push_candidate({"id": candidate_info["id"], "chineseName": tip_candidate_name})
    if not candidate_info:
        data = await gle_push_app.candidate_app.put_candidate_under_job_order_by_info(
            job_order=job_order_info["id"],
            phone=tip_phone,
            email=tip_email,
            name=tip_candidate_name,
            overwrite_entity=candidate
        )
        logger.info(f"候选人不存在 id->{data} 执行创建候选人操作")

