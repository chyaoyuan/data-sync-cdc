import json
with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/project_id/project_map_candidate.jsonl",'r') as f:
    while line := f.readline():
        print(json.loads(line))
        break