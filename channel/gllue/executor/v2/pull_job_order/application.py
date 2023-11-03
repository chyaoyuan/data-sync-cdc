import asyncio
from channel.gllue.executor.base.application import GleExeApp
from channel.gllue.executor.v2.cgl_config import CGLConfig

if __name__ == '__main__':
    _sync_config = {
        "syncModel": CGLConfig.SyncModel.Recent,
        "storageModel": "Tip",  # Local # Tip
        "unit": "day",
        "recent": 3,
        "timeFieldName": "lastUpdateDate__day_range",
        **CGLConfig.entity_job_order,
        "extraFieldNameList": "jobsubmission__candidate__id,citys",
        "extraGql": "is_private__s=0",
}

    g = GleExeApp(CGLConfig.gle_user_config,
                  {"syncModel": _sync_config["syncModel"]},
                  _sync_config,
                  CGLConfig.tip_config_prod)
    asyncio.run(g.sync())
