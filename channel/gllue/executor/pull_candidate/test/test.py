import asyncio
import json

import aiohttp
from TipConvert import ConvertApp
from loguru import logger

from channel.gllue.pull.application.applicaiton import GlePullApplication
from channel.gllue.pull.application.candidate.application import GleCandidateApplication
from middleware.external.application import external_application

if __name__ == '__main__':
    gle_user_config_ = {
        "apiServerHost": "https://www.cgladvisory.com",
        "aesKey": "398b5ec714c59be2",
        "account": "system@wearecgl.com",
        "extraPassword": "Xue727511",
        "extraAccount":"system@wearecgl.com"
    }
    base_sync_config_ = {
        "syncModel": "Id",
        "syncAttachment": False,
    }
    sync_config = {
        "syncAttachment": False,
        "storageModel": "Local",
        "jsonFileStorageName": "res_20231007.jsonl",
        "FileStoragePath": "res_20231007.jsonl",
        "startTime": "2023-08-01 00:00:00",
        "endTime": "2023-09-01 00:00:00",
        "recent": "1",
        "unit": "month",
        "timeFieldName": "dateAdded__day_range",
        "idList": [],
        "idRecent": [],
        "convertId": "Resume:standard:2023_09_04_03_27_59",
        "fieldList": ["attachments", "tags", "functions", "industrys", "locations", ],
    }


    async def execute():
        async with aiohttp.ClientSession() as session:
            convert_app = ConvertApp(session, {"convertServerHost": "http://converter.nadileaf.com"})
            gle_pull_app = GlePullApplication(gle_user_config_, base_sync_config_)
            field_name_list: str = await gle_pull_app.candidate_app.initialize_field()
            id_list = [str(i) for i in range(2557620, 2560145)]
            task_list = await gle_pull_app.candidate_app.create_tasks(field_name_list, id_list)
            for candidate_task in asyncio.as_completed(task_list):
                entity_list, source_response = await candidate_task
                for entity in entity_list:
                    logger.info(entity)
                    std_entity, _ = await convert_app.convert(["Resume:standard:2023_09_04_03_27_59"], entity)
                    logger.info(f"source->{entity}")
                    logger.info(f"converted->{std_entity}")
                    std_entity["source"] = "谷露"
                    await external_application.transmitter_app.save_data({
                        "tenant": "shanghaidezhuqiyeguanli-188",
                        "entityType": "Resume",
                        "entityId": std_entity['resumeID'],
                        "entity": {
                            "customFields": {
                                "detectedSourceUrl": f"https://www.cgladvisory.com/crm/candidate/detail?id={std_entity['resumeID'].replace('gllue-', '')}"},
                            "standardFields": std_entity,
                            "rawData": {
                                "content": entity
                            }
                        },
                        "source": "Gllue-CGL-Resume",
                        "editor": "data-sync-cdc",
                    })
    asyncio.run(execute())