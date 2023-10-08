import asyncio
import json

import aiofiles
import aiohttp
from loguru import logger


async def execute():
    data_list = []
    index = 0
    with open("/Volumes/Expansion/res.jsonl", "r") as f:
        while line := f.readline():
            try:
                content = json.loads(line)
                logger.info(content)
            except Exception as e:
                continue
            if len(content.keys()) == 1:

                _id = content["id"]
                data_list.append(int(_id))
    logger.info("count")
    logger.info(len(data_list))
    data_list = list(set(data_list))
    logger.info(len(data_list))
    with open("/Volumes/Expansion/gllue_not_exist_candidate_id_20230928.json","w") as f3:
        f3.write(json.dumps(data_list, ensure_ascii=False))

if __name__ == '__main__':
    asyncio.run(execute())