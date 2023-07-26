import json

with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/project_id/project_map_candidate.jsonl",
          "r") as f3:
    success_project_id_list = []
    while line := f3.readline():
        data = json.loads(line)
        success_project_id_list.append(data["projectId"])

print(len(success_project_id_list))
print(len(set(success_project_id_list)))
