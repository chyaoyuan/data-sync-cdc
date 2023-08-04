import json


with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/applicant/data/project_id_list.json", "r") as f2:
    full_project_id_list: list[str] = json.loads(f2.read())

# with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/project_id/project_map_candidate.jsonl", "r") as f3:
#     success_project_id_list = []
#     while line := f3.readline():
#         data = json.loads(line)
#
#         success_project_id_list.append(data["projectId"])
#     success_project_id_list = list(set(success_project_id_list))

# need_run_project_list = list(set(full_project_id_list) - set(success_project_id_list))
print(len(full_project_id_list))
count = len(full_project_id_list) // 4
print(count)


with open(f"/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/applicant/data/project_id_1.json", "w") as f2:
    f2.write(json.dumps(full_project_id_list[0:count], ensure_ascii=False))
with open(f"/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/applicant/data/project_id_2.json", "w") as f2:
    f2.write(json.dumps(full_project_id_list[count+1:count*2], ensure_ascii=False))
with open(f"/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/applicant/data/project_id_3.json", "w") as f2:
    f2.write(json.dumps(full_project_id_list[count*2+1:count*3], ensure_ascii=False))
with open(f"/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/applicant/data/project_id_4.json", "w") as f2:
    f2.write(json.dumps(full_project_id_list[count*3+1:], ensure_ascii=False))