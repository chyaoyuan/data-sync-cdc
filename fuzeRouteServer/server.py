import json
import os
from typing import List

import aiohttp
import jmespath
import requests
import uvicorn
from fastapi import FastAPI

from channel.gllue.executor.upsert_candidate_to_job_order.upsert_candidate_to_job_order import \
    upsert_candidate_to_job_order
from utils.logger import logger
from TipConvert import ConvertApp

from channel.gllue.executor.model import GleUserConfig, SyncConfig
from channel.gllue.executor.push_job_order.push_job_order import push_gle_job_order_executor
from fuzeRouteServer.fuzeModel.stage_update import stage_up_date_body
from fuzeRouteServer.fuzeModel.taskModel import EventMessage, EventBody
from fuzeRouteServer.normalModel.transmitterModel import TransmitterRequestModel, EntityModel, EntityConvertModel
from fuzeRouteServer.settings.settings import Settings

app = FastAPI(
    title="Fze转换转发服务",
    description="将Fuze的body经过转换和提取转发到不同pod"
)
convert_config = {
    "default": {"gllueEntityPush": {
        "Job": os.getenv("JobConvert", None),
        "Project": os.getenv("ProjectConvert", None),
        "Resume": os.getenv("CandidateConvert", "ResumeCgl:standard:2023_09_26_02_19_16"),
        "BusinessPartner": os.getenv("CandidateConvert", None),
    }}
}


def get_entity(entity_list: List[EntityModel], entity_type: str):
    for entity in entity_list:
        if entity.entityType == entity_type:
            return entity


def get_converted_entity(entity_list: List[EntityConvertModel], entity_type: str):
    for entity in entity_list:
        if entity.entityType == entity_type:
            return entity


_sync_config = {
        "syncModel": "Id",
        "entityName": "jobOrder",
        "recent": "30",
        "unit": "year",
        "timeFieldName": "lastUpdateDate__day_range",
        "gql": "jobStatus__s=Live",
        "fieldNameList": "operation,id,client__name,client__candidate_authorization_remind,islimited,jobTitle,client__name,client__type,client____name__,client__is_parent,client__parent,client__parent__id,client__parent__type,client,jobStatus,longlist_count,cvsent_count,clientinterview_count,offersign_count,addedBy__user,addedBy__type,addedBy,joborderuser_set__user____name__,joborderuser_set__type,joborderuser_set,gllueextcharge,workflow_spec__addedBy____name__,workflow_spec__addedBy,dateAdded,__name__,citys,positionType,gllueextFeerate",
        "childEntityList": [{
            "gql": None,
            "entityName": "jobSubMission"
        }],

    }


@app.post("/v1/{channel}/{upstream}")
async def run(channel: str, upstream: str, event: str, fuze_body: dict):
    print(channel)
    print(upstream)
    print(event)
    channel = "gllue"
    upstream = "fuze"
    event = "status-changes"
    logger.info(json.dumps(fuze_body, ensure_ascii=False))
    fuze_body = EventBody(**fuze_body)
    extra_config = {k: v["value"] for k, v in json.loads(fuze_body.data).items()}
    project = TransmitterRequestModel(
        **{"tenantAlias": fuze_body.eventMessage.tenantId,
           "openId": fuze_body.eventMessage.newTask.standardFields.project.openId,
           "entityType": fuze_body.eventMessage.newTask.standardFields.project.entityType})

    candidate = TransmitterRequestModel(
        **{"tenantAlias": fuze_body.eventMessage.tenantId,
           "openId": fuze_body.eventMessage.newTask.standardFields.taskPayload.openId,
           "entityType": fuze_body.eventMessage.newTask.standardFields.taskPayload.entityType})
    entities: List[EntityModel] = []
    for _body in [project, candidate]:
        res = requests.get(Settings.TransmitterSettings.transmitterUrl.format(**_body.dict()))
        assert res.status_code == 200
        entities.append(EntityModel(**{**_body.dict(), "body": res.json()}))

    job = TransmitterRequestModel(
        **{"tenantAlias": fuze_body.eventMessage.tenantId,
           "openId": get_entity(entities, "Project").body["data"]["standardFields"]["projectPayload"]["openId"],
           "entityType": get_entity(entities, "Project").body["data"]["standardFields"]["projectPayload"][
               "entityType"]})

    res = requests.get(Settings.TransmitterSettings.transmitterUrl.format(**job.dict()))
    assert res.status_code == 200
    entities.append(EntityModel(**{**job.dict(), "body": res.json()}))
    # business_partner = TransmitterRequestModel(
    #     **{"tenantAlias": fuze_body.eventMessage.tenantId,
    #        "openId": get_entity(entities, "Job").body["data"]["standardFields"]["headhunterRequestDetail"]["partyA"][
    #            "openId"],
    #        "entityType": get_entity(entities, "Job").body["data"]["standardFields"]["headhunterRequestDetail"]["partyA"][
    #            "entityType"]})
    # res = requests.get(Settings.TransmitterSettings.transmitterUrl.format(**business_partner.dict()))
    # entities.append(EntityModel(**{**business_partner.dict(), "body": res.json()}))
    entities_res: List[EntityConvertModel] = []
    async with aiohttp.ClientSession() as session:
        c = ConvertApp(session, {"convertServerHost": os.getenv("convertServerHost", "http://converter.nadileaf.com")})
        for entity in entities:
            if entity.entityType == "Resume":
                converted_entity, status = await c.convert(["ResumeCgl:standard:2023_09_26_02_19_16"], entity.body.get("data",{}).get("standardFields",{}))
                logger.info(converted_entity)
                entities_res.append(EntityConvertModel(**{**entity.dict(), "convertBody": converted_entity}))
            else:
                entities_res.append(EntityConvertModel(**{**entity.dict(), "convertBody": entity.body}))
    logger.info(f"transmitter success->{json.dumps([_.dict() for _ in entities_res],ensure_ascii=False)}")

    result = await upsert_candidate_to_job_order(
        GleUserConfig(**extra_config),
        SyncConfig(**_sync_config),
        get_converted_entity(entities_res, "Job"),
        get_converted_entity(entities_res, "Resume"))
    return result


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9300)
