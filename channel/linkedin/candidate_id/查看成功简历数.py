import json
candidate_id_list = []
with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/candidate_id/success_candidate.jsonl","r") as f:
    while line := f.readline():
        data = json.loads(line)
        candidate_id = data["candidateId"]
        candidate_id_list.append(candidate_id)
print(len(candidate_id_list))
print(len(set(candidate_id_list)))
print(len(candidate_id_list)-len(set(candidate_id_list)))