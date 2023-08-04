import json

with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/project_id/un_repeat_project_map_candidate.jsonl") as f:
    while line := f.readline():
        data = json.loads(line)
        if data["projectId"] == "432223697":
            print(data)
