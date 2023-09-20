import asyncio
from typing import Literal, Optional, List
import aiohttp
import uvicorn
from fastapi import FastAPI

from channel.gllue.executor.push_job_order.push_job_order import push_gle_job_order_executor
from channel.gllue.pull.application.applicaiton import GlePullApplication
from channel.gllue.session.gllue_aiohttp_session import GlHoMuraSession
from gllueEntityPushServer.model import GlePushEntityModel, EntityConvertModel

app = FastAPI(
    title="谷露实体推送服务",
    description="输入谷露的实体，根据预设规则将该实体更新/新增到谷露系统上"
)


def get_entity_info(entity_body_list: List[EntityConvertModel],entity_type: str):
    for entity_body in entity_body_list:
        if entity_body.entityType == entity_type:
            return entity_body


@app.post("/v1/GllueEntity/Push/AutoCreate")
async def auto_push(body: GlePushEntityModel):
    await push_gle_job_order_executor(
        GleUserConfig(**extra_config),
        SyncConfig(**_sync_config),
        get_converted_entity(entities_res, "BusinessPartner").convertBody,
        get_converted_entity(entities_res, "Job").convertBody,
        get_converted_entity(entities_res, "Resume").convertBody
    )



if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9400)
