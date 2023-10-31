import asyncio

from channel.gllue.executor.base.application import GleExeApp
from channel.gllue.executor.v2.cgl_config import CGLConfig

if __name__ == '__main__':

    _sync_config = {
          **CGLConfig.base_sync_config_GqlFilter,
        "storageModel": "Tip",  # Local # Tip
        "gql": "jobsubmission_set__cvsent_set__date__isnull|(mobile__isnull&has_attachment__eq=1&note_set__isnull=&tags__isnull)",
        **CGLConfig.entity_candidate,
}
    _sync_config = {
        "syncModel": CGLConfig.SyncModel.IdList,
        "storageModel": "Tip",  # Local # Tip
        "idList": [2567085],
        **CGLConfig.entity_candidate,
        "extraFieldNameList": "jobsubmission__candidate__id,citys",
    }
    g = GleExeApp(CGLConfig.gle_user_config, {"syncModel": _sync_config["syncModel"]}, _sync_config, CGLConfig.tip_config)
    asyncio.run(g.sync())

