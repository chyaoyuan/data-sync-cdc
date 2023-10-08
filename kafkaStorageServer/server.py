import asyncio
import json
from typing import Optional, Literal, List

import uvicorn
from loguru import logger
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from kafkaStorageServer.application import AIOKafkaProducerSession
from kafkaStorageServer.settings.settings import Settings

app = FastAPI()


class InsertBody(BaseModel):
    kafkaHeader: Optional[dict] = Field(default={})
    kafkaKey: str = Field(default="")
    kafkaContent: dict


producer = None

@app.on_event("startup")
async def startup_event():
    global producer
    producer = AIOKafkaProducerSession(Settings.KafkaSettings.BootstrapServers)
    await producer.init_producer()


@app.put("/v1/{topic}/write")
async def insert_kafka(topic: str, body: InsertBody):
    global producer
    if topic not in Settings.KafkaSettings.AllowTopics:
        raise HTTPException(status_code=400, detail="Invalid topic")
    await producer.send(topic, value=body.kafkaContent, key=body.kafkaKey)
    logger.info(f"topic->{topic} key->{body.kafkaKey}")
    return


@app.put("/v1/{topic}/batch-write")
async def insert_kafka(topic: str, body_list: List[InsertBody]):
    global producer
    if topic not in Settings.KafkaSettings.AllowTopics:
        raise HTTPException(status_code=400, detail="Invalid topic")
    await asyncio.gather(
        *[
            producer.send(topic, value=body.kafkaContent, key=body.kafkaKey,) for body in body_list
        ]
    )
    logger.info(f"topic->{topic} key->{[i.kafkaKey for i in body_list]}")
    return

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=Settings.ServerPort)
