import json
un_repect_project_id_list = []
with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/project_id/project_map_candidate.jsonl","r") as f3:
    while line := f3.readline():
        data = json.loads(line)
        print(1111)
        if data["projectId"] not in un_repect_project_id_list:
            with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/project_id/un_repeat_project_map_candidate.jsonl", "a") as f4:
                f4.write(json.dumps(data, ensure_ascii=False))
                f4.write("\n")
                un_repect_project_id_list.append(data["projectId"])

print(len(un_repect_project_id_list))