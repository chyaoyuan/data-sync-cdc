from channel.gllue.pull.application.candidate.application import GleEntity
from channel.gllue.pull.application.client.application import GlePullClient


class GlePullApplication:
    def __init__(self, user_config: dict, sync_config: dict):
        self.user_config = user_config
        self.sync_config = sync_config
        self.candidate_app = GleEntity(self.user_config, self.sync_config)
        self.client_app = GlePullClient(self.user_config)
