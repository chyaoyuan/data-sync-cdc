import asyncio
import json

import aiofiles
import aiohttp
from loguru import logger


async def execute(data_list, session):
    _ = await session.put(
        "https://data-sync-kafka-storage-server.mesoor.com/v1/cgl_gllue_candidate_to_transmitter/batch-write", ssl=False,
        json=data_list)
    logger.info(_.status)
    logger.info(await _.text())

async def run():
    async with aiohttp.ClientSession() as session:
        index = 0
        async with aiofiles.open("/Users/chenjiabin/Project/data-sync-cdc/channel/gllue/executor/pull_candidate/res_20231007.jsonl","r") as f:
            data_list = []
            while line := f.readline():
                logger.info(bool(line))
                content = json.loads(await line)

                if len(content.keys()) == 1:
                    continue
                if len(data_list) < 1000:
                    _ = {
                        # "kafkaHeader": {"convert": True, "convertId": "Resume:standard:2023_09_04_03_27_59", "tenant": "cgltest","entityType": "Resume", "openId": entity_id,"X-Source":"gllue","X-Editor":"data-sync-cdc"},
                        "kafkaKey": "gllue-candidate-" + str(content.get("id")),
                        "kafkaContent": content
                    }
                    data_list.append(_)

                else:
                    logger.info(f"index->{index}")
                    if index < 0:
                        data_list = []
                        index = index + 1
                        continue
                    await execute(data_list, session)
                    index = index + 1
                    data_list = []
            if len(data_list) < 1000:
                await execute(data_list, session)

if __name__ == '__main__':
    asyncio.run(run())
