import json

from aiokafka import AIOKafkaProducer


class AIOKafkaProducerSession:
    def __init__(self, bootstrap_servers: str):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda v: v.encode('utf-8'))

    async def init_producer(self):
        await self.producer.start()

    async def send(self, topic: str, value, key: str):
        await self.producer.send(topic, value, key)

    # @property
    # def to_aio_kafka(self, **kv):
    #     result = []
    #     for key, value in kv.items():
    #         if isinstance(value, bytes):
    #             continue
    #         if isinstance(value, str):
    #             new_value = value
    #         elif isinstance(value, dict) or isinstance(value, list):
    #             new_value = json.dumps(value, ensure_ascii=False)
    #         elif isinstance(value, bool):
    #             new_value = str(int(value))
    #         else:
    #             new_value = str(value)
    #         result.append((key, new_value.encode()))
    #     return result

if __name__ == '__main__':
    pass