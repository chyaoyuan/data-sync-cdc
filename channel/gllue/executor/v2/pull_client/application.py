import asyncio
import json

from channel.gllue.executor.base.application import GleExeApp
from channel.gllue.executor.v2.cgl_config import CGLConfig

if __name__ == '__main__':
    with open("/Users/chenjiabin/Project/data-sync-cdc/channel/gllue/check/BusinessPartner/clientNeedRun.json") as f:
        data = json.loads(f.read())

    _sync_config = {
        "syncModel": CGLConfig.SyncModel.IdList,
        "storageModel": "Tip",  # Local # Tip
        "idList": data,
        "unit": "day",
        "recent": 3,
        "timeFieldName": "lastUpdateDate__day_range",
        # "extraGql": "type__ns=generated",
        **CGLConfig.entity_client,
}


    g = GleExeApp(CGLConfig.gle_user_config, {"syncModel": _sync_config["syncModel"]}, _sync_config, CGLConfig.tip_config_prod)
    asyncio.run(g.sync())
