import asyncio

from channel.gllue.executor.base.application import GleExeApp
from channel.gllue.executor.v2.cgl_config import CGLConfig

if __name__ == '__main__':

    _sync_config = {
        "syncModel": "GqlFilter",
        "storageModel": "Tip",  # Local # Tip
        "gql": "keyword=2560556",
        "childFieldList": ["note"],
        **CGLConfig.entity_candidate,
}

    g = GleExeApp(CGLConfig.gle_user_config, CGLConfig.base_sync_config_GqlFilter, _sync_config, CGLConfig.tip_config)
    asyncio.run(g.sync())
