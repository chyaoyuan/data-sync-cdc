from typing import Optional, Literal, List
from channel.gllue.pull.application.attachment.application import GleAttachment
from channel.gllue.pull.application.entity.application import GleEntityApplication
from channel.gllue.pull.application.model.sync_model import BaseSyncConfig
from channel.gllue.pull.application.schema.application import GleSchema


class GleClientContractApplication(GleEntityApplication):

    entityType: str = "clientcontract".lower()
    total_count: int = 5

    def __init__(self, gle_user_config: dict, base_sync_config: dict):
        super().__init__(gle_user_config, base_sync_config)
        self.base_sync_config = BaseSyncConfig(**base_sync_config)
        self.schema_config = {}
        self.candidate_function_map = {}
        # schema
        self.schema_app = GleSchema(gle_user_config)
        # 附件
        self.attachment_app = GleAttachment(gle_user_config)
        # 用户/操作者
        self.gle_user_id: Optional[int] = None

    async def init_schema(self):
        await self.schema_app.initialize_field_map_field(self.entityType)

    # def create_source_url(self, entity_path: str):
    #     # 合同没有展示页所以贴上公司链接
    #     if jmespath.search("partA")
    #         return f"{self.gle_user_config.apiServerHost}/crm/client/detail?id={params['clientId']}"

    def create_extra_entity_id_map(self, result: dict):
        entity_type_list = list(result.keys())
        entity_type_list.remove(self.entityType)
        new_map = {}
        for entity_type in entity_type_list:
            new_map[entity_type] = self.schema_app._create_extra_entity_id_map(result)
        return new_map
