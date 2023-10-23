import asyncio

from channel.gllue.executor.base.application import GleExeApp


class GlePullUser(GleExeApp):

    pass


if __name__ == '__main__':
    _gle_user_config = {
        "apiServerHost": "https://www.cgladvisory.com",
        "aesKey": "398b5ec714c59be2",
        "account": "system@wearecgl.com",
    }
    base_sync_config = {
        "syncModel": "TimeRange",
        "syncAttachment": False,
    }
    _sync_config = {
        "primaryEntityName": "user",
        "syncModel": "TimeRange",
        "storageModel": "Local",
        "storagePath": "./data",
        "orderBy": "id",
        "startTime": "2023-08-01 00:00:00",
        "endTime": "2023-09-01 00:00:00",
        "recent": "1",
        "unit": "month",
        "timeFieldName": "dateAdded__day_range",
        "convertId": "Resume:standard:2023_09_04_03_27_59",

    }
    g = GlePullUser(_gle_user_config,base_sync_config, _sync_config)
    asyncio.run(g.sync())
