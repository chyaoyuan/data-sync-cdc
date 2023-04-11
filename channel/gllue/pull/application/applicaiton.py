from typing import Type

from channel.gllue.config import Settings
from channel.gllue.pull.application.candidate.application import GleCandidate
from channel.gllue.pull.application.jobOrder.application import GleJobOrder


class GlePullApplication:
    def __init__(self, settings: dict):
        self.settings = settings
        self.candidate_app = GleCandidate(settings)
        self.job_order_app = GleJobOrder(settings)