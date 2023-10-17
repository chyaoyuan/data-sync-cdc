import asyncio

from channel.gllue.executor.base.application import GleExeApp


class GlePullClientContract(GleExeApp):

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
        "primaryEntityName": "clientContract".lower(),
        "tipEntityName": "Contract",
        "syncModel": "TimeRange",
        "storageModel": "Local",
        "jsonFileStorageName": "gllue_client_contract_2013_10_16.jsonl",
        "storagePath": "./data",
        "orderBy": "id",
        "startTime": "2023-08-01 00:00:00",
        "endTime": "2023-09-01 00:00:00",
        "recent": "1",
        "unit": "month",
        "timeFieldName": "dateAdded__day_range",
        "convertId": "cgltest:gllue:gllue_client_contract_to_Contract",

    }
    tip_config = {
        "tenantAlias": "bklj6280h0y7x"
    }
    g = GlePullClientContract(_gle_user_config,base_sync_config, _sync_config,tip_config)
    asyncio.run(g.sync())
