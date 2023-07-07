from channel.gllue.application.candidate.application import GleEntity
from channel.gllue.application.client.application import GleClient


class GlePullApplication:
    def __init__(self, user_config: dict, sync_config:dict):
        self.user_config = user_config
        self.sync_config = sync_config
        self.candidate_app = GleEntity(self.user_config, self.sync_config)
        self.client_app = GleClient(self.user_config)
