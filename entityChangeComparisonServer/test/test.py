import json

import jmespath

{
    "tenant": "ALL",
    "entity": "GllueCandidate",
    "From": "Gllue",
    "to": "dataSyncEntityStorage",
    "fieldConfig":
        [{
            "field": "attachment[0].uuidname",
            "type": "change",
            "not": False
        },{
            "field": "attachment[0].uuidname",
            "type": "change",
            "not": False
        }]

}
with open("/Users/chenjiabin/Project/data-sync-cdc/entityChangeComparisonServer/data/gllue_candidate_1_before.json") as f:
    before = json.loads(f.read())


with open("/Users/chenjiabin/Project/data-sync-cdc/entityChangeComparisonServer/data/gllue_candidate_1_after.json") as f:
    after = json.loads(f.read())

b = jmespath.search("attachment[0].uuidname",before)
print(b)