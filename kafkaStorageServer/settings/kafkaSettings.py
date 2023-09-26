import os


class KafkaSettings:
    BootstrapServers = os.getenv("BootstrapServers", "http://localhost:9092")
    AllowTopics: list = os.getenv("AllowTopics", "cgl_gllue_candidate_to_transmitter").split(",")
