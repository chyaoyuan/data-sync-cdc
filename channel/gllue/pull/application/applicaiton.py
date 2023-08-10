from channel.gllue.pull.application.candidate.application import GleEntity
from channel.gllue.pull.application.client.application import GlePullClient
from channel.gllue.pull.application.jobOrder.application import GleJobOrder
from channel.gllue.pull.application.jobSubMission.application import GleJobSubMissionInfo
from channel.gllue.pull.application.schema.application import GleSchema


class GlePullApplication:
    def __init__(self, user_config: dict, sync_config: dict):
        # gle 的基础配置
        self.user_config = user_config
        # gle 同步配置
        self.sync_config = sync_config
        # tip系统配置
        self.tip_config = {}

        self.schema_app = GleSchema(self.user_config)
        self.candidate_app = GleEntity(self.user_config, self.sync_config)
        self.client_app = GlePullClient(self.user_config)
        self.job_order_app = GleJobOrder(self.user_config)
        self.job_sub_mission_app = GleJobSubMissionInfo(self.user_config)
