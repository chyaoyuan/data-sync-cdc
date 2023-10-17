import asyncio
from asyncio import Task
from typing import Optional
from urllib.parse import urlencode
from urllib.parse import quote
import requests

from fuzeRouteServer.normalModel.transmitterModel import EntityConvertModel
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


async def upsert_candidate_to_job_order(gle_user_config: GleUserConfig,
                                        sync_config: SyncConfig,
                                        job_order: EntityConvertModel,
                                        candidate: EntityConvertModel):
    """
    同步谷露的职位(jobOrder)
    根据配置同步子关联实体[职位下候选人](jobSubMission)
    """
    logger.info(job_order)
    logger.info(candidate)
    gle_job_order_id = int(job_order.openId.replace("gllue-", ""))

    # Job
    tip_email = jmespath.search("data.standardFields.contactInfo.personalEmail", candidate.body)
    tip_phone = jmespath.search("data.standardFields.contactInfo.mobilePhoneNumber", candidate.body)

    gle_pull_app = GlePullApplication(gle_user_config.dict(), sync_config.dict())
    gle_push_app = GlePushApplication(gle_user_config.dict())

    # 如果是谷露简历，只和项目做关联
    # 这里就不检查
    if "gllue-" in candidate.openId:
        gle_candidate_id = int(candidate.openId.replace("gllue-", ""))
        await gle_push_app.job_order_app.put_candidate_under_job_order_by_id(
            job_order_id=gle_job_order_id,
            candidate_id_list=[gle_candidate_id]
        )

        return True
    # 如果是来源tip的，手机号和邮箱必有一个
    if not tip_phone and not tip_email:
        return {"message": f"候选人{candidate.openId}缺少手机号和邮箱不回写谷露系统"}
    candidate_info = await gle_pull_app.candidate_app.get_candidate_by_contact_gql({"mobile": tip_phone, "email": tip_email})
    if candidate_info:
        # if not await gle_pull_app.job_sub_mission_app.check_candidate_in_job_order_by_job_order_id(gle_job_order_id, candidate_info["id"]):
        #     await gle_push_app.job_order_app.put_candidate_under_job_order_by_candidate_id(gle_job_order_id, candidate_list=[candidate_info["id"]])
        #     logger.info(f"候选人已存在但未关联 client_id->{gle_job_order_id} job_id->{gle_job_order_id} candidate_id->{candidate_info['id']} 执行移动候选人到项目下操作")
        # else:
        #     logger.info(f"候选人已存在已关联 client_id->{gle_job_order_id} job_id->{gle_job_order_id} candidate_id->{candidate_info['id']} 不执行操作")
        logger.info(f"gle_job_order_id->{gle_job_order_id}")
        logger.info(f"gle_candidate_id->{candidate_info}")
        await gle_push_app.job_order_app.put_candidate_under_job_order_by_id(gle_job_order_id, candidate_id_list=[candidate_info["id"]])
    else:
        data = await gle_push_app.candidate_app.put_candidate_under_job_order_by_info(
            {"job_order": gle_job_order_id},
            candidate.convertBody
        )
        logger.info(f"候选人不存在 id->{data} 执行创建候选人操作")
        await gle_push_app.job_order_app.put_candidate_under_job_order_by_id(gle_job_order_id,
                                                                             candidate_id_list=[data])

