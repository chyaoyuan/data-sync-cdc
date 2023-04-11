import asyncio
from typing import Literal

from channel.gllue.pull.application.schema.model import GleSchemaUrl
from channel.gllue.pull.application.base.application import BaseApplication


class GleSchema(BaseApplication):
    def __init__(self, gle_user_config: dict):
        super().__init__(gle_user_config)

    # 获取schema
    async def get_schema(self, typeName: Literal["Candidate", "Position"]):
        url = GleSchemaUrl(typeName=typeName, apiServerHost=self.gle_user_config.apiServerHost).get_schema
        # channel/gllue/application/Schema/data/candidate_schema.json
        res, status = await self.async_session.get(url=url,
                                                   ssl=False,
                                                   gle_config=self.gle_user_config.dict(),
                                                   func=self.request_response_callback)
        return res

    async def get_field_name_list(self, typeName: Literal["Candidate", "Position", "JobOrder"]):
        res = await self.get_schema(typeName=typeName)
        # field_name_list = [typeName+"__"+_["name"]for _ in res]
        field_name_list = [_["name"] for _ in res]
        return field_name_list


if __name__ == '__main__':
    asyncio.run(GleSchema({
            "apiServerHost": "https://fsgtest.gllue.net",
            "aesKey": "824531e8cad2a287",
            "account": "api@fsg.com.cn"
        }).get_field_name_list(typeName="Candidate"))