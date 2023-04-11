import os

env_dist = os.environ
class Settings:
    server_port = int(env_dist.get("SERVER_PORT", "8091"))
