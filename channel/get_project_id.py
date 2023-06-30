import json

with open (file="/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/project_info_list.jsonl",mode="r") as f:
    while line := f.readline():
        print(line)
        break
        body = json.loads(line)
        for _ in body:
            id = _["data"]["data"]["hiringProjectsByCriteria"]["*elements"]
            print(id)