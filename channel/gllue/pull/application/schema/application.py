import asyncio

from loguru import logger

from channel.gllue.pull.application.schema.model import GleSchemaUrl
from channel.gllue.pull.application.base.application import BaseApplication


class GleSchema(BaseApplication):
    def __init__(self, gle_user_config: dict):
        super().__init__(gle_user_config)

    async def get_schema(self, type_name: str):
        # 获取schema
        url = self.settings.get_entity_schema_url.format(apiServerHost=self.gle_user_config.apiServerHost, entityType=type_name).lower()
        # example: channel/gllue/application/Schema/data/candidate_schema.json
        res, status = await self.async_session.get(url=url, ssl=False, func=self.request_response_callback)

        if isinstance(res, dict) and res["message"]:
            raise Exception(f"获取gleSchema失败->{type_name} {status} {url} {res}")
        return res

    async def get_field_name_list(self, type_name: str):
        res = await self.get_schema(type_name=type_name)
        logger.info(res)
        field_name_list = [_["name"] for _ in res]
        return field_name_list

    async def get_field_name_list_child(self, type_name: str):
        res = await self.get_schema(type_name=type_name)

        field_name_list = [type_name + "_set__" + _["name"] for _ in res]
        return list(set(field_name_list))

    @staticmethod
    def get_field_name_list_child_from_field_list(field_list: list):
        # 因为子字段和夫级字段都在一个层级，所以这个函数用来从字段列表中把子字段的抽取出来
        # 然后合并到对应实体下
        _field_name_child_list = []
        for field_name in field_list:
            if "_set__" in field_name:
                child_field_name = field_name.split("_set__")[0]

                _field_name_child_list.append(child_field_name)
        return _field_name_child_list

    @staticmethod
    def get_field_name_list_child_from_res(entity_id: str, entity_name: str,  source: list) -> list:
        if not source:
            return []
        entity_source = []
        for _ in source:
            if _[entity_name] == entity_id:
                entity_source.append(_)
        return entity_source

    @staticmethod
    def map_host_to_url(entity: dict, host: str):
        map_key_config_set = ("__download_oss_url", "__oss_url")
        if entity.get("attachment") or None:
            for attachment in entity.get("attachment"):
                for map_key_config in map_key_config_set:
                    if map_key_config in attachment.keys():
                        attachment[map_key_config] = host+attachment[map_key_config]


if __name__ == '__main__':
    _field_name_list = asyncio.run(GleSchema({
            "apiServerHost": "https://fsgtest.gllue.net",
            "aesKey": "824531e8cad2a287",
            "account": "api@fsg.com.cn"
        }).get_field_name_list(type_name="industry"))
    print(_field_name_list)