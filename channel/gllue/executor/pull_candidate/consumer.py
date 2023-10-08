import json
import os
from middleware.external.application import external_application
import aiohttp
from loguru import logger
from aiokafka import AIOKafkaConsumer
import asyncio
from TipMidApp.TipConvert import ConvertApp
topic_name: str = os.getenv("TopicName", "cgl_gllue_candidate_to_transmitter")
bootstrap_servers: str = os.getenv("BootstrapServers", "dev-kafka-kafka-brokers.infra.svc:9092")
group_id: str = os.getenv("GroupId", "test-1")
tenant_alias: str = os.getenv("tenantAlias", "cgltest")
rule_engine_server: str = os.getenv("RULE_ENGINE_SERVER", "http://dev-ruleengine")


async def execute(convert_app, msg):
    while True:
        try:
            std_entity, _ = await convert_app.convert("Resume:standard:2023_09_04_03_27_59", json.loads(msg.value))
            if "resumeID" not in std_entity.keys():
                logger.error(f"转换有误原数据->{json.loads(msg.value)}")
                logger.error(f"转换有误转换结果->{std_entity}")
                logger.error(f"转换有误转换详情->{_}")
                return
            logger.info(f"source->{json.loads(msg.value)}")
            logger.info(f"converted->{std_entity}")
            std_entity["source"] = "谷露"
            await external_application.transmitter_app.save_data({
                "tenant": tenant_alias,
                "entityType": "Resume",
                "entityId": std_entity['resumeID'],
                "entity": {
                    "customFields": {
                        "detectedSourceUrl": f"https://www.cgladvisory.com/crm/candidate/detail?id={std_entity['resumeID'].replace('gllue-', '')}"},
                    "standardFields": std_entity,
                    "rawData": {
                        "content": json.loads(msg.value)
                    }
                },
                "source": "Gllue-CGL-Resume",
                "editor": "data-sync-cdc",
            })
            return
        except Exception as e:
            logger.error(e)
            await asyncio.sleep(3)
            pass



async def consumer():
    async with aiohttp.ClientSession() as session:
        convert_app = ConvertApp(session, {"ConvertServerHost": "http://converter.nadileaf.com"})
        logger.info("init")
        _consumer = AIOKafkaConsumer(
            topic_name,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id)
        await _consumer.start()
        while True:
            logger.info("start")
            data_list = []
            async for msg in _consumer:
                if len(data_list) < 100:
                    data_list.append(msg)
                else:
                    await asyncio.gather(*[execute(convert_app, msg) for msg in data_list])
                    data_list = []
            logger.info("batch")



if __name__ == '__main__':

    asyncio.run(consumer())