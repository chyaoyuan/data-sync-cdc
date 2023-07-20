import json

with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/project_id_list.json", "r") as f2:
    project_id_list: list[str] = json.loads(f2.read())

    with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/success_project_id_list.jsonl", "r") as f3:
        success_project_id_list = []
        while line := f3.readline():
            data = json.loads(line)
            success_project_id_list.append(data["id"])
            success_project_id_list = list(set(success_project_id_list))
    # 去除成功的project_id
    for success_project_id in success_project_id_list:
        project_id_list.pop(success_project_id)
    for index, data in enumerate(project_id_list):
        print(index)