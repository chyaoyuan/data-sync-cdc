import asyncio
import json

import aiofiles
import aiohttp
from loguru import logger


async def execute():
    with open("/Volumes/Expansion/gllue_not_exist_candidate_id_20230928.json", "r") as f2:
        not_exist_id = [str(i) for i in json.loads(f2.read())]

    with open("/Volumes/Expansion/gllue_candidate_in_tip_20230928.json", "r") as f:
        id_list = json.loads(f.read())

        max_ = max(id_list)
        logger.info(max_)
        min_ = min(id_list)
        logger.info(min_)
        maybe_exist_id = set([str(i) for i in range(min_, max_ + 1)]) - set([str(i) for i in id_list]) - set(not_exist_id)
        logger.info(len(maybe_exist_id))



        # full_id =
        # logger.info(len(full_id))
        # with open("/Volumes/Expansion/gllue_not_exist_candidate_id_20230928.json", "r") as f2:
        #     not_exist_id = set(json.loads(f2.read()))
        #     last_id = full_id-not_exist_id
        #     logger.info(last_id)
        #     logger.info(type(last_id))
        with open("/Volumes/Expansion/gllue_maybe_exist_candidate_id_20230928.json", "w") as f3:
            f3.write(json.dumps(list(maybe_exist_id),ensure_ascii=False))

if __name__ == '__main__':
    asyncio.run(execute())