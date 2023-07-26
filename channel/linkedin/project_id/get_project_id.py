import json
_all = []
with open(file="/channel/linkedin/project_id/project_info_list.jsonl", mode="r") as f:
    while line := f.readline():
        body = json.loads(line)
        project_id = body["data"]["data"]["hiringProjectsByCriteria"].get("*elements")
        if not project_id:

            break
        _all = _all + project_id
project_id_list = list(set(_all))
new_list = []
for project in project_id_list:
    new_list.append(project.split(",")[-1].replace(")", ""))
with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/project_id_list.json", "w") as f2:
    f2.write(json.dumps(list(set(new_list)),ensure_ascii=False))
    print(len(list(set(new_list))))
