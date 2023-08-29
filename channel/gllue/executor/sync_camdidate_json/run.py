import asyncio

from channel.gllue.executor.sync_camdidate_json.sync_candidate import sync_candidate_pull_and_push

_gle_user_config = {
    "apiServerHost": "https://www.cgladvisory.com",
    "aesKey": "398b5ec714c59be2",
    "account": "system@wearecgl.com"
}
_gle_user_config = {
    "apiServerHost": "https://fsgtest.gllue.net",
    "aesKey": "824531e8cad2a287",
    "account": "api@fsg.com.cn"
}
_sync_config = {
    "entity": "candidate",
    "recent": "5",
    "unit": "day",
    "timeFieldName": "lastUpdateDate__day_range",
    "gql": None,
    "fieldList": ["attachments", "tags", "functions", "industrys", "locations"],
    "childFieldList": ["candidateexperience", "candidateproject", "candidateeducation", "candidatelanguage", "candidatequalification"]
}
# _sync_config = {
#     "entity": "candidate",
#     "recent": "3",
#     "unit": "day",
#     "timeFieldName": "lastUpdateDate__lastUpdateDate__day_range",
#     "gql": None,
#
# }

asyncio.run(sync_candidate_pull_and_push(_gle_user_config, _sync_config))