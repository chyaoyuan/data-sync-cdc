import os

from kafkaStorageServer.settings.kafkaSettings import KafkaSettings


class Settings:
    KafkaSettings = KafkaSettings
    ServerPort: int = os.getenv("ServerPort", 9200)
