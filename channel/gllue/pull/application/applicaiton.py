from channel.gllue.pull.application.candidate.application import GleCandidateApplication
# from channel.gllue.pull.application.client.application import GlePullClient
from channel.gllue.pull.application.client.application import GlePullClient
from channel.gllue.pull.application.clientcontract.application import GleClientContractApplication
from channel.gllue.pull.application.entity.application import GleEntityApplication
from channel.gllue.pull.application.invoice.application import GlePullInvoice
from channel.gllue.pull.application.jobOrder.application import GleJobOrder
from channel.gllue.pull.application.jobSubMission.application import GleJobSubMissionInfo
from channel.gllue.pull.application.schema.application import GleSchema
from channel.gllue.pull.application.user.application import GleUserApplication


class GlePullApplication:
    def __init__(self, gle_user_config: dict, base_sync_config: dict):
        # gle 的基础配置
        self.gle_user_config = gle_user_config
        # gle 同步配置
        self.base_sync_config = base_sync_config
        self.schema_app = GleSchema(self.gle_user_config)
        self.base_entity_in_used = GleEntityApplication(self.gle_user_config, self.base_sync_config)

        self.candidate_app = GleCandidateApplication(self.gle_user_config, self.base_sync_config)
        self.client_app = GlePullClient(self.gle_user_config, self.base_sync_config)

        self.invoice_app = GlePullInvoice(self.gle_user_config, self.base_sync_config)
        self.joborder_app = GleJobOrder(self.gle_user_config, self.base_sync_config)
        self.jobsubmission_app = GleJobSubMissionInfo(self.gle_user_config, self.base_sync_config)
        self.user_app = GleUserApplication(self.gle_user_config, self.base_sync_config)
        self.clientcontract_app = GleClientContractApplication(self.gle_user_config, self.base_sync_config)

    def get_app(self, entity_name: str):
        app_attribute_name = f"{entity_name}_app"
        if hasattr(self, app_attribute_name):
            return getattr(self, app_attribute_name)
        else:
            raise ValueError(f"Invalid entity_name: {entity_name}")
