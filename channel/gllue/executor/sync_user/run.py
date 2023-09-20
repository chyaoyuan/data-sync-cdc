import asyncio
from channel.gllue.executor.sync_user.sync_user import sync_user_exe
filed_list = "operation,avatar,baseuser____name__,baseuser,id,englishName,chineseName,__name__,name,englishName,isleader,team____name__,team,title____name__,title,email,status,joinInDate,leaveDate,gllueext_date_1546670858937,mobile,__name__,profile,isleader,gllueext_select_1609990945128,gllueext_WeCom,gllueextCGLID,officeTel,dateOfBirth,dataaccessgroup,chineseName,accessgroup,baseuser__profile____name__,baseuser__profile,gllueext_ranking_1596512455993,gllueext_ranking_1596512563587,agent,gllueext_coin_haitunbalance,gllueext_coin_haituntotal,team2____name__,team2,team3____name__,team3,dateAdded,gllueext_starting_date_EC,gllueext_end_date_EC,lastUpdateDate,lastUpdateBy_id"

_gle_user_config = {
    "apiServerHost": "https://www.cgladvisory.com",
    "aesKey": "398b5ec714c59be2",
    "account": "system@wearecgl.com"
}
# _gle_user_config = {
#     "apiServerHost": "https://fsgtest.gllue.net",
#     "aesKey": "824531e8cad2a287",
#     "account": "api@fsg.com.cn"
# }
_sync_config = {
    "entity": "candidate",
    "syncModel": "Recent",
    "syncAttachment": False,
    # "startTime": "2022-07-14",
    "startTime": "2023-03-11",
    "endTime": "2023-09-05",
    "orderBy": "id",
    "recent": "50",
    "unit": "year",
    "timeFieldName": "dateAdded__day_range",
    "gql": None,
    "convertId": "Resume:standard:2023_09_04_03_27_59",
    "fieldList": ["attachments", "tags", "functions", "industrys", "locations", "candidateexperience_set__client__name"],
    "childFieldList": ["candidateeducation"],
    # "childFieldList": ["candidateeducation", "candidateexperience", "candidateproject", "candidatelanguage", "candidatequalification"],
    "idList": [],
    # "childFieldList": ["candidateexperience", "candidateproject", "candidatelanguage", "candidatequalification"],
    "onlyMarge": [
        "/standardFields/humanInfo/name"]
 }
# _sync_config = {
#     "entity": "candidate",
#     "recent": "3",
#     "unit": "day",
#     "timeFieldName": "lastUpdateDate__lastUpdateDate__day_range",
#     "gql": None,
#
# }

asyncio.run(sync_user_exe(_gle_user_config, _sync_config))