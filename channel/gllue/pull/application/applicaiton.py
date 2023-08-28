from channel.gllue.pull.application.candidate.application import GleEntity
from channel.gllue.pull.application.client.application import GlePullClient
from channel.gllue.pull.application.jobOrder.application import GleJobOrder
from channel.gllue.pull.application.jobSubMission.application import GleJobSubMissionInfo
from channel.gllue.pull.application.schema.application import GleSchema


class GlePullApplication:
    def __init__(self, gle_user_config: dict, sync_config: dict):
        # gle 的基础配置
        self.gle_user_config = gle_user_config
        # gle 同步配置
        self.sync_config = sync_config
        self.schema_app = GleSchema(self.gle_user_config)
        self.candidate_app = GleEntity(self.gle_user_config,self.sync_config)
        self.client_app = GlePullClient(self.gle_user_config, self.sync_config)
        self.job_order_app = GleJobOrder(self.gle_user_config,self.sync_config)
        self.job_sub_mission_app = GleJobSubMissionInfo(self.gle_user_config)

