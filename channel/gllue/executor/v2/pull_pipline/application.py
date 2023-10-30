import asyncio

from channel.gllue.executor.base.application import GleExeApp
from channel.gllue.executor.v2.cgl_config import CGLConfig

if __name__ == '__main__':

    _sync_config = {
        "syncModel": CGLConfig.SyncModel.IdList,
        "storageModel": "Tip",  # Local # Tip
        "idList": [3447292],

        **CGLConfig.entity_jobsubmission,
        "extraFieldNameList": "jobsubmission__candidate__id,citys",
        "extraEntity": [
            CGLConfig.entity_candidate, CGLConfig.entity_job_order
        ]
    }
    g = GleExeApp(CGLConfig.gle_user_config,
                  {"syncModel": _sync_config["syncModel"]},
                  _sync_config,
                  CGLConfig.tip_config)
    asyncio.run(g.sync())
