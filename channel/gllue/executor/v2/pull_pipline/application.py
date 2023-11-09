import asyncio

from channel.gllue.executor.base.application import GleExeApp
from channel.gllue.executor.v2.cgl_config import CGLConfig

if __name__ == '__main__':
    _sync_config = {
        "syncModel": CGLConfig.SyncModel.IdList,
        "storageModel": ["tip"],  # Local # Tip
        "unit": "day",
        "recent": 3,
        "idList": [3402589, 3402590, 3402591, 3402592, 3402593, 3402594, 3402595, 3402596, 3402597, 3402598, 3402599, 3402600, 3402601, 3402602, 3402603, 3402604, 3402605, 3402606, 3402607, 3402608, 3402609, 3402610, 3402611, 3402612, 3402613, 3402614, 3402615, 3402616, 3402617, 3402618, 3402620, 3402621, 3402622, 3402623, 3402624, 3402625, 3402626, 3402627, 3402628, 3402629, 3402630, 3402631, 3402632, 3402633, 3402634, 3402635, 3402636, 3402637, 3402638, 3402639, 3402640, 3402641, 3402642, 3402643, 3402644, 3402645, 3402646, 3402647, 3402648, 3402649, 3402650, 3402651, 3402652, 3402653, 3402654, 3402655, 3402656, 3402657, 3402658, 3402659, 3402660, 3402661, 3402662, 3402663, 3402664, 3402665, 3402666, 3402668, 3402669, 3402670, 3402671, 3402672, 3402673, 3402674, 3402675, 3402676, 3402677, 3402678, 3402679, 3402680, 3402681, 3402682, 3402683, 3402684, 3402685, 3402686, 3402687, 3402688, 3402689, 3402690],
        "timeFieldName": "lastUpdateDate__day_range",
        **CGLConfig.entity_jobsubmission,
        "extraGql": "joborder__is_private__s=0",
        "extraFieldNameList": "jobsubmission__candidate__id,citys",
        # "extraEntity": [
        #     CGLConfig.entity_candidate, CGLConfig.entity_job_order, CGLConfig.entity_job_order
        # ]
    }

    g = GleExeApp(CGLConfig.gle_user_config,
                          {"syncModel": _sync_config["syncModel"]},
                          _sync_config,
                          CGLConfig.tip_config_prod)
    asyncio.run(g.sync())
