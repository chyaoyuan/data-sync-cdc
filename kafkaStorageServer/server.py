import asyncio
import json
from typing import Optional, Literal, List

import uvicorn
from loguru import logger
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from pydantic import BaseModel, Field

from kafkaStorageServer.settings.settings import Settings

app = FastAPI()


class InsertBody(BaseModel):
    kafkaHeader: Optional[dict] = Field(default={})
    kafkaKey: str = Field(default="")
    kafkaContent: dict


producer = None


@app.put("/v1/{topic}/write")
async def insert_kafka(topic: Literal["cgl_gllue_candidate_to_transmitter"], body: InsertBody):
    assert topic in Settings.KafkaSettings.AllowTopics
    global producer
    if not producer:
        producer = AIOKafkaProducer(
            bootstrap_servers=Settings.KafkaSettings.BootstrapServers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    await producer.start()
    await producer.send_and_wait(topic, value=body.kafkaContent, key=body.kafkaKey, headers=body.kafkaHeader)

    await producer.stop()
    logger.info(f"topic->{topic} key->{body.kafkaKey}")
    return


@app.put("/v1/{topic}/batch-write")
async def insert_kafka(topic: Literal["cgl_gllue_candidate_to_transmitter"], body: List[InsertBody]):
    assert topic in Settings.KafkaSettings.AllowTopics
    global producer
    if not producer:
        producer = AIOKafkaProducer(
            bootstrap_servers=Settings.KafkaSettings.BootstrapServers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    await producer.start()
    await asyncio.gather(
        *[producer.send_and_wait(topic, value=_.kafkaContent, key=_.kafkaKey, headers=_.kafkaHeader)for _ in body]
    )
    await producer.stop()
    logger.info(f"topic->{topic} key->{[i.kafkaKey for i in body]}")
    return

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=Settings.ServerPort)