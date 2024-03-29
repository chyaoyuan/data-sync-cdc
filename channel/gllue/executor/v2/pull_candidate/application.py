import asyncio
import json

from channel.gllue.executor.base.application import GleExeApp
from channel.gllue.executor.v2.cgl_config import CGLConfig

if __name__ == '__main__':

    _sync_config = {
        "syncModel": CGLConfig.SyncModel.Recent,
        "storageModel": ["tip"],
        "unit": "day",
        "recent": 3,
        "timeFieldName": "lastUpdateDate__day_range",
        "extraFieldNameList": "citys",
        **CGLConfig.entity_candidate,
    }
    g = GleExeApp(CGLConfig.gle_user_config, {"syncModel": _sync_config["syncModel"]}, _sync_config, CGLConfig.tip_config_prod)
    asyncio.run(g.sync())

