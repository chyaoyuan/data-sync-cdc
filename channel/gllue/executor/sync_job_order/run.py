import asyncio
from channel.gllue.executor.model import GleUserConfig, SyncConfig, TipConfig
from channel.gllue.executor.sync_job_order.sync_job_order import sync_gle_job_executor

sync = "cgl"


assert sync in ["waifu", "cgl"]
if sync == "waifu":
    _gle_user_config = {
        "apiServerHost": "https://fsgtest.gllue.net",
        "aesKey": "824531e8cad2a287",
        "account": "api@fsg.com.cn"
    }
    _sync_config = {
        "entityName": "jobOrder",
        "recent": "30",
        "unit": "year",
        "timeFieldName": "lastUpdateDate__day_range",
        "gql": "jobStatus__s=Live",
        # "fieldNameList": "operation,id,client__name,client__candidate_authorization_remind,islimited,jobTitle,client__name,client__type,client____name__,client__is_parent,client__parent,client__parent__id,client__parent__type,client,jobStatus,longlist_count,cvsent_count,clientinterview_count,offersign_count,addedBy__user,addedBy__type,addedBy,joborderuser_set__user____name__,joborderuser_set__type,joborderuser_set,gllueextcharge,workflow_spec__addedBy____name__,workflow_spec__addedBy,dateAdded,__name__,citys,positionType,gllueextFeerate",
        "childEntityList": [{
            "gql": None,
            "entityName": "jobSubMission"
        }],

    }
elif sync == "cgl":
    _gle_user_config = {
        "apiServerHost": "https://www.cgladvisory.com",
        "aesKey": "398b5ec714c59be2",
        "account": "system@wearecgl.com"
    }
    _sync_config = {
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
else:
    _gle_user_config = {}
    _sync_config = {}


_tip_config = {
       "jwtToken": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VybmFtZTo4NjE3NjEyMzA1NzE2IiwidGVuYW50SWQiOjEwMDAxNDksImlzcyI6ImRlZmF1bHQiLCJ0ZW5hbnRBbGlhcyI6Im5iMWwxMDAwMTQ5cXo1NXgiLCJleHAiOjE2OTI4NjMyNzg0MjksInVzZXJJZCI6IjJhOGZmNjE2LTZlMTQtNDQ2MS04YjRkLTJhM2ZkZDAxOTMzNyIsInByb2plY3RJZCI6ImRlZmF1bHQiLCJpYXQiOjE2OTE2NTM2Nzg0Mjl9.d9F4MKQq_kv7AKbTq3YdrSTZrhTqPmQhEQTS7mrb0nw",
       "spaceId": "5ea8b9c6-373f-4641-8f3f-07cc46128ed9",
}

asyncio.run(
    sync_gle_job_executor(
        GleUserConfig(**_gle_user_config),
        SyncConfig(**_sync_config),
        TipConfig.transform(_tip_config)
    )
)