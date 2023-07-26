import json
with open("/channel/linkedin/project_id/candidate_list.jsonl", "r") as f3:
    success_project_id_list = []
    while line := f3.readline():
        data = json.loads(line)
        success_project_id_list.append(data["projectId"])
    success_project_id_list = list(set(success_project_id_list))
print(len(success_project_id_list))

import json
with open("/channel/linkedin/project_id/project_id_list.json", "r") as f3:
    c = json.loads(f3.read())
    print(len(c))