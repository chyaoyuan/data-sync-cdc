import asyncio
from channel.gllue.executor.base.application import GleExeApp
from channel.gllue.executor.base.field_remap import config_map
from channel.gllue.executor.v2.cgl_config import CGLConfig

if __name__ == '__main__':
    _sync_config = {
        **CGLConfig.gle_user_config,
        "syncModel": CGLConfig.SyncModel.IdRecent,
        "storageModel": ["tip"],  # Local # Tip
        "IdRecent": "0-30000",
        "primaryEntityName": CGLConfig.EntityName.invoice,
        "tenantAlias": CGLConfig.tip_config_prod,

    }

    g = GleExeApp(*config_map(_sync_config))
    asyncio.run(g.sync())
