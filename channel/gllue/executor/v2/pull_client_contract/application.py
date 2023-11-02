import asyncio

from channel.gllue.executor.base.application import GleExeApp
from channel.gllue.executor.v2.cgl_config import CGLConfig

if __name__ == '__main__':

    _sync_config = {
        "syncModel": CGLConfig.SyncModel.Recent,
        "unit": "day",
        "recent": 3,
        "timeFieldName": "lastUpdateDate__day_range",
        "storageModel": "Tip",  # Local # Tip
        **CGLConfig.entity_contract,
        "extraFieldNameList": "citys",
}
    g = GleExeApp(CGLConfig.gle_user_config, {"syncModel": _sync_config["syncModel"]}, _sync_config, CGLConfig.tip_config_prod)
    asyncio.run(g.sync())
