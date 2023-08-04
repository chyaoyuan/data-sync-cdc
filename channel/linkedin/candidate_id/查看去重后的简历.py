import json


candidate_id_list = []
upper = False
lower = False
with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/candidate_id/unrepeat_candidate_info.jsonl", "r") as f:
    index = 0
    while line := f.readline():
        _info: dict = json.loads(line)
        if _info["candidateId"] in ["AEMAAB5mrwwBKkD3qF8CHniTEwM2xjnPqMvABSE"]:
            print(_info)
        if (upper and lower and upper <= index <= lower) or _info["candidateId"] in ["AEMAAB5mrwwBKkD3qF8CHniTEwM2xjnPqMvABSE"]:
            print(_info)



