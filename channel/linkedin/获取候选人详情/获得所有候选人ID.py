import json

from loguru import logger

candidate_id_list = []

with open("/channel/linkedin/project_id/candidate_list.jsonl", "r") as f3:
    success_project_id_list = []
    while line := f3.readline():
        try:
            data = json.loads(line)
        except Exception as e:
            continue
        _candidate_list = data.get("candidate_list", [])
        for index, _candidate_info in enumerate(_candidate_list):
            _id = _candidate_info["skillsMatchInsightUrn"]
            print(_id)
            candidate_id_list.append(_id)
finally_result = list(set(candidate_id_list))
print(len(finally_result))
# spli = len(finally_result) // 4
#
# # for candidate_id in list(set(candidate_id_list)):
# #     print(candidate_id)
# with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/candidate_id/candidate_1.json","w") as f:
#     f.write(json.dumps(finally_result[:spli]))
#
# with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/candidate_id/candidate_2.json","w") as f:
#     f.write(json.dumps(finally_result[spli+1:spli*2]))
#
# with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/candidate_id/candidate_3.json","w") as f:
#     f.write(json.dumps(finally_result[spli*2+1:spli*3]))
#
# with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/candidate_id/candidate_4.json","w") as f:
#     f.write(json.dumps(finally_result[spli*3+1:]))