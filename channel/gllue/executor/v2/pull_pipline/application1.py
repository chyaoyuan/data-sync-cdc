import asyncio

from channel.gllue.executor.base.application import GleExeApp
from channel.gllue.executor.v2.cgl_config import CGLConfig

if __name__ == '__main__':

    _sync_config = {
        "syncModel": CGLConfig.SyncModel.IdList,
        "storageModel": "Tip",  # Local # Tip
        "idList": [1],
        "unit": "day",
        "recent": 3,
        "timeFieldName": "lastUpdateDate__day_range",
        "gql": "lastUpdateDate__day_range=2023-10-27%2C2023-10-31",
        **CGLConfig.entity_jobsubmission,
        "extraFieldNameList": "jobsubmission__candidate__id,citys",
        # "extraEntity": [
        #     CGLConfig.entity_candidate, CGLConfig.entity_job_order
        # ]
    }
    g = GleExeApp(CGLConfig.gle_user_config,
                  {"syncModel": _sync_config["syncModel"]},
                  _sync_config,
                  CGLConfig.tip_config_prod)
    asyncio.run(g.sync())
