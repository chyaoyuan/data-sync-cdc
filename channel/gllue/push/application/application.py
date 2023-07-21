from channel.gllue.push.application.candidate.application import GlePushCandidate
from channel.gllue.push.application.client.application import GlePushClient


class GlePushApplication:
    def __init__(self, gle_user_config: dict):
        self.user_config = gle_user_config
        self.candidate_app = GlePushCandidate(self.user_config)
        self.client_app = GlePushClient(self.user_config)