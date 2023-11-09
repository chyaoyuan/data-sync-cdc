import asyncio

from channel.gllue.executor.base.application import GleExeApp
from channel.gllue.executor.base.field_remap import config_map
from channel.gllue.executor.v2.cgl_config import CGLConfig

if __name__ == '__main__':
    _sync_config = {
        **CGLConfig.gle_user_config,
        "syncModel": CGLConfig.SyncModel.Recent,
        "storageModel": ["tip"],  # Local # Tip
        "unit": "day",
        "timeFieldName": "lastUpdateDate__day_range",
        "recent": 3,
        "tenantAlias": CGLConfig.tip_config_prod,
        "primaryEntityName": CGLConfig.EntityName.jobsubmission,
    }

    g = GleExeApp(*config_map(_sync_config))
    asyncio.run(g.sync())
