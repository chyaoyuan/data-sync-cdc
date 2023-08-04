import json
from loguru import logger
candidate_id_list = []
with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/candidate_id/unrepeat_candidate_info.jsonl","a") as f2:
    with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/candidate_id/success_candidate.jsonl","r") as f:
        while line := f.readline():
            data = json.loads(line)
            candidate_id = data["candidateId"]
            if candidate_id not in candidate_id_list:
                logger.info(f"add->{candidate_id}")
                f2.write(json.dumps(data, ensure_ascii=False)+"\n")
                candidate_id_list.append(candidate_id)
            else:
                logger.info(f"skip->{candidate_id}")


# print(f"含重复简历数->{len(candidate_id_list)}")
# print(f"成功简历数->{len(set(candidate_id_list))}")
# with open("/Users/chenjiabin/Project/data-sync-cdc/channel/linkedin/candidate_id/success_candidate_id.jsonl","a") as f:
#
#     for candidate_id in list(set(candidate_id_list)):
#         f.write(json.dumps({"candidateId": candidate_id}, ensure_ascii=False))
#         f.write("\n")

