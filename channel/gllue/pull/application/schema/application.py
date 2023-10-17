import asyncio
import copy
import json
from typing import Optional, List

import aiohttp
import requests

from channel.gllue.pull.application.base.application import BaseApplication
from channel.gllue.pull.application.schema.model import SchemaFieldInfo, GleFieldType
from utils.logger import logger
from asgiref.sync import async_to_sync

import addressparser


class GleSchema(BaseApplication):
    # 谷露需要进行ID转换的字段
    # system_field_name_list = ["function", "industry", "city", "team", "channel", "profile"]
    system_field_name_list = ["function", "industry", "city"]
    # 当检查到子实体有存在entity_list内的引用关系时，会自动添加字段
    # 比如候选人工作经历candidateexperience的schema里有candidateexperience_set__client
    entity_list = []

    def __init__(self, gle_user_config: dict):
        super().__init__(gle_user_config)
        self.init_job_order_schema: Optional[list] = []
        # 谷露有些字段是ID，这里获取所有的这种结构的字段并展平，为id转文本相互转换使用，用于写入tip和推送和打标签
        # 例子来源：外服谷露系统，不同客户格式一致，值会有差异，这里走的是自动获取并转换
        # example channel/gllue/pull/application/schema/exampleData/field_id_map.json
        self.field_id_map = {}
        # example channel/gllue/pull/application/schema/exampleData/filed_string_map.json
        self.field_string_map = {}
        #
        self.source_entity_schema = None

    def flatten_json(self, json_data, flat_dict=None):
        if flat_dict is None:
            flat_dict = {}
        for item in json_data:
            flat_dict[item["id"]] = item["name"]
            if "children" in item and item["children"]:
                self.flatten_json(item["children"], flat_dict)

        return flat_dict

    def flatten_json_1(self, json_data: list, father_field_name: Optional[str] = None, flat_dict: Optional[dict] = None):
        """打平字段"""
        if not flat_dict:
            flat_dict = {}
        for item in json_data:
            if father_field_name:
                field_name = f"{father_field_name}-{item['name']}"
            else:
                field_name = f"{item['name']}"
            flat_dict[field_name] = item["id"]
            if "children" in item and item["children"]:
                self.flatten_json_1(item["children"], field_name, flat_dict)

        return flat_dict

    @staticmethod
    def _create_extra_entity_id_map(entity_list):
        """将同时同步过来的其它实体生成map"""
        return {_["id"]: _ for _ in entity_list}

    def mesoor_extra(self, data, extra_entity_map: dict, field_name_list: list):
        if isinstance(data, dict):
            to_update = {}
            for key, value in data.items():
                if key and value:
                    if key in field_name_list:
                        if isinstance(value, bool):
                            value = "true" if value else "false"
                        new_key = f"mesoorExtra{key.capitalize()}"
                        if key in extra_entity_map and isinstance(value, dict) and value in extra_entity_map[key]:
                            to_update[new_key] = extra_entity_map[key][value]
                        elif key in extra_entity_map.keys() and isinstance(value, (int, str)) and value in \
                                extra_entity_map[
                                    key].keys():
                            to_update[new_key] = extra_entity_map[key][value]

                    elif key.endswith('s') and key[: -1] in field_name_list:
                        key_singular = key[: -1]
                        new_key = f"mesoorExtra{key.capitalize()}"
                        if key_singular in extra_entity_map.keys() and isinstance(value, list):
                            cache_value = []
                            for _ in value:

                                cache_value.append(extra_entity_map[key_singular][_])
                            to_update[new_key] = cache_value

            data.update(to_update)
            for key, value in data.items():
                self.mesoor_extra(value, extra_entity_map, field_name_list)
        elif isinstance(data, list):
            for item in data:
                self.mesoor_extra(item, extra_entity_map, field_name_list)
        return data

    def merge_fields(self,entity_type, source_entity_list: list, child_field_name_list: list, result):
        entity_list = []
        for index, candidate in enumerate(source_entity_list):
            entity_id = candidate["id"]
            entity = {**candidate}
            for child_field_name in child_field_name_list:
                _ = self.get_field_name_list_child_from_res(entity_id, entity_type, result.get(child_field_name))
                entity[child_field_name] = _
            entity_list.append(entity)
        return entity_list

    async def initialize_field_map_field(self, entity_name: str):
        entity_schema = await self.get_schema(entity_name)
        logger.info(entity_schema)
        for field_schema in entity_schema:
            name = field_schema["name"]
            map_dict = {}
            if (options := field_schema.get("options", [])) and isinstance(options, list):
                for option in options:
                    if (code := option.get("code")) and (value := option.get("value")):
                        map_dict[code] = value
                    if not self.field_id_map.get(entity_name):
                        self.field_id_map[entity_name] = {}
                    if not self.field_string_map.get(entity_name):
                        self.field_string_map[entity_name] = {}
                    self.field_string_map[entity_name][name] = {v: k for k, v in map_dict.items()}
                    self.field_id_map[entity_name][name] = {k: v for k, v in map_dict.items()}
                logger.info(f"schema 字段map生成->{entity_name} -> {name}")
        for file_name in self.system_field_name_list:
            url = self.settings.get_field_schema_url.format(entityType=file_name)
            res, status = await self.async_session.get(url, func=self.request_response_callback)
            if isinstance(res, dict) and (message := res.get("message")):
                logger.error(f"无法加载字段详情 将去除token重新请求->{file_name} {message}")
                res, status = await self.async_session.get(url, not_use_token=True, func=self.request_response_callback)
                if isinstance(res, dict) and (message := res.get("message")):
                    logger.error(f"最终无法加载字段详情->{file_name} {message}")
                    continue

            # 城市无法直接对应，需要转换成中间格式
            if file_name == "city":
                _ = {}
                city_string_map = self.flatten_json_1(res)
                self.field_id_map[file_name] = {_id: name for name, _id in city_string_map.items()}
                self.field_id_map["location"] = {_id: name for name, _id in city_string_map.items()}

                for location_str, gle_id in city_string_map.items():
                    x = addressparser.transform([location_str]).iloc[0]
                    name = f"{x['省']}-{x['市']}-{x['区']}"
                    _[name] = gle_id
                    # 城市不需要

                self.field_id_map[file_name] = {_id: name for name, _id in _.items()}
                self.field_string_map[file_name] = _

            else:
                self.field_id_map[file_name] = self.flatten_json(res, {})
                self.field_string_map[file_name] = self.flatten_json_1(res)
            logger.info(f"系统字段map生成->{file_name}")
        return self.field_id_map, self.field_string_map

    async def get_schema(self, type_name: str):
        # 获取实体 schema
        url = self.settings.get_entity_schema_url.format(entityType=type_name).lower()
        fields_info, status = await self.async_session.get(url=url, func=self.request_response_callback)
        if isinstance(fields_info, dict) and fields_info["message"]:
            raise Exception(f"获取谷露Schema失败->{type_name} {status} {url} {fields_info}")
        logger.info(f"获取schema成功->{type_name} ")
        return fields_info

    async def get_model_map_group(self):
        url = self.settings.get_entity_schema_url.format(entityType="model_map_group").lower()
        model_map, _ = await self.async_session.get(url, func=self.request_response_callback)
        _dict = {}
        for k, v in model_map.items():
            if v not in _dict.keys():
                _dict[v] = []
            _dict[v].append(k)
        return _dict, model_map


    async def get_foreignkey(self, type_name: str):
        # 只拿到lv2就不递归，两层循环解决
        new_filed_list = []
        logger.error(type_name)
        field_info_list = await self.get_schema(type_name=type_name)
        field_info_list = [SchemaFieldInfo(**info) for info in field_info_list]
        for field_info in field_info_list:
            if field_info.type == "foreignkey" and field_info.name != type_name:
                lv2_field_info_list = await self.get_schema(type_name=field_info.name)
                if lv2_field_info_list:
                    # new_filed_list.append(f"{field_info.name}____name__")
                    new_filed_list.append(f"{field_info.name}__set__")
        logger.error(new_filed_list)
        return new_filed_list





    async def get_field_name_list(self, type_name: str):
        res = await self.get_schema(type_name=type_name)
        field_name_list = [_["name"] for _ in res]
        logger.info(field_name_list)
        return field_name_list

    async def get_field_name_list_child(self, type_name: str):
        field_info_list: List[dict] = await self.get_schema(type_name=type_name)
        logger.info(field_info_list)
        # 不干啥，，就是简单定义下model
        _field_info_list: List[SchemaFieldInfo] = [SchemaFieldInfo(**info) for info in field_info_list]
        field_name_list = [f"{type_name}_set__{_.name}" for _ in _field_info_list]
        foreign_key_field_name_list = [f"{type_name}_set__{_.name}__name" for _ in _field_info_list if _.type == "foreignkey"]
        logger.error(foreign_key_field_name_list)
        return list(set(field_name_list + foreign_key_field_name_list))

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

    async def get_quick_search_group(self, entity_type: str):
        """获取快速GQL，用于客户想填写GQL但是不会填GQL的场景"""
        # 这个是GQL的实体类型
        gql_entity_type = "QuickSearchGroup".lower()
        res, _ = await self.async_session.get(
            url=self.settings.get_entity_url.format(entityType=gql_entity_type),
            params={
                "page": 1,
                "gql": f"model_name={entity_type}&active=true",
                "fields": "id,name,builtin,active,gql",
                "paginate_by": 50},
            func=self.request_response_callback,
            ssl=False
        )
        quick_search_groups = res.get("result", {}).get(gql_entity_type, [])
        self.field_string_map[gql_entity_type] = {qs["name"]: qs["id"] for qs in quick_search_groups}
        self.field_string_map[gql_entity_type] = {qs["id"]: qs["name"] for qs in quick_search_groups}
        return quick_search_groups

    def get_city_id_by_location_string(self, location: str):
        x = addressparser.transform([location]).iloc[0]
        i = f"{x['省']}-{x['市']}-{x['区']}"
        logger.info(i)
        return self.field_string_map['city'].get(i)

    async def get_field_trans_map(self, field_name_list: str):
        # 用于获得英文中文字段映射
        form_data = aiohttp.FormData()
        form_data.add_field("ids", field_name_list)
        # ids: joborder^id,joborder^lineManager,joborder^function
        res, status = await self.async_session.post("/rest/code_file/batch_field_trans_map",
                                                    data=form_data,

                                                    token=False,
                                                    func=self.request_response_callback)
        logger.info(res)

    async def test(self):
        url = "/rest/customlistsetting/get_default_setting?model=candidate&scene=normal&user_id=2491&appscene_id=1"
        res, _ = await self.async_session.get(url, ssl=False, func=self.request_response_callback)
        logger.info(res)


if __name__ == '__main__':
    config = {
        "apiServerHost": "https://fsgtest.gllue.net",
        "aesKey": "824531e8cad2a287",
        "account": "api@fsg.com.cn"
        }
    config = {
        "apiServerHost": "https://www.cgladvisory.com",
        "aesKey": "398b5ec714c59be2",
        "account": "system@wearecgl.com"
}
    a = GleSchema(config)
    field_id_map, field_string_map = asyncio.run(a.initialize_field_map_field("candidate"))
    # logger.info(field_id_map)
    # logger.info(field_string_map)



