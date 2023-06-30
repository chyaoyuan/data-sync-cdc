import asyncio
from typing import Literal

from loguru import logger

from channel.gllue.pull.application.schema.model import GleSchemaUrl
from channel.gllue.pull.application.base.application import BaseApplication


class GleSchema(BaseApplication):
    def __init__(self, gle_user_config: dict):
        super().__init__(gle_user_config)

    # 获取schema
    async def get_schema(self, type_name: str):
        url = GleSchemaUrl(typeName=type_name, apiServerHost=self.gle_user_config.apiServerHost).get_schema
        # channel/gllue/application/Schema/data/candidate_schema.json
        res, status = await self.async_session.get(url=url,
                                                   ssl=False,
                                                   gle_config=self.gle_user_config.dict(),
                                                   func=self.request_response_callback)
        logger.info(res)
        return res

    async def get_field_name_list(self, type_name: str):
        res = await self.get_schema(type_name=type_name)
        field_name_list = [_["name"] for _ in res]
        # logger.info(f"字段展示{typeName}->{field_name_list}")
        return field_name_list

    async def get_field_name_list_child(self, type_name: str):
        res = await self.get_schema(type_name=type_name)

        field_name_list = [type_name + "_set__" + _["name"] for _ in res]
        logger.info(f"子字段展示{type_name}->{field_name_list}")
        return field_name_list

    @staticmethod
    def get_field_name_list_child_from_field_list(field_list: list):
        # 因为子字段和夫级字段都在一个层级，所以这个函数用来从字段列表中把子字段的抽取出来
        # 然后合并到对应实体下
        # 举例

        _field_name_child_list = []
        for field_name in field_list:
            if "_set__" in field_name:
                child_field_name = field_name.split("_set__")[0]
                _field_name_child_list.append(child_field_name)
        return _field_name_child_list


if __name__ == '__main__':
    _field_name_list = asyncio.run(GleSchema({
            "apiServerHost": "https://fsgtest.gllue.net",
            "aesKey": "824531e8cad2a287",
            "account": "api@fsg.com.cn"
        }).get_field_name_list_child(type_name="candidateeducation"))
    print(_field_name_list)