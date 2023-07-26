import json


candidate_id_list = []

with open("/channel/linkedin/project_id/project_map_candidate.jsonl", "r") as f:
    index = 0
    while line := f.readline():
        project_info: dict = json.loads(line)
        candidate_info_list: list = project_info.get("candidate_list", [])
        for candidate_info in candidate_info_list:
            candidate_id_list.append(candidate_info["skillsMatchInsightUrn"])

print(len(candidate_id_list))
print(len(set(candidate_id_list)))