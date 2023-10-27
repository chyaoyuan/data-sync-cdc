import asyncio

from channel.gllue.executor.base.application import GleExeApp
from channel.gllue.executor.v2.cgl_config import CGLConfig

if __name__ == '__main__':

    _sync_config = {
        "syncModel": CGLConfig.SyncModel.GqlFilter,
        "storageModel": "Tip",  # Local # Tip
        "gql": "status__hasvalue",
        "IdRecent": "25000-30000",
        **CGLConfig.entity_job_order,
        "extraFieldNameList": "jobsubmission__candidate__id,citys",
        "extraEntity": [
            CGLConfig.entity_job_order,
        ]}
    g = GleExeApp(CGLConfig.gle_user_config,
                  {"syncModel": _sync_config["syncModel"]},
                  _sync_config,
                  CGLConfig.tip_config)
    asyncio.run(g.sync())
