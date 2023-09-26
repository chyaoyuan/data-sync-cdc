import re

from TipMidApp import TipMidApplication
from loguru import logger

from channel.gllue.pull.application.schema.application import GleSchema


class FunctionApplication:
    def __init__(self, schema: GleSchema):
        self.schema: GleSchema = schema

        self.tip_app = TipMidApplication(None, {})

    def map(self, func_name: str, string: str):
        if "id_map" in func_name:
            return self.id_map(func_name, string)
        return getattr(self, func_name.lower(), None)(string)

    def salary(self, string: str) -> str:
        return self.tip_app.field_normalization_app.salary_range(string)

    @staticmethod
    def get_int(string: str) -> str:
        c2 = re.search(r'\d+', string)
        return c2.group()

    def id_map(self, path: str, string: str):
        logger.info(string)
        logger.info(path)
        path_list = path.replace("id_map", "").split(".")
        cache = None
        for path in path_list:
            if not cache:
                cache = self.schema.field_string_map.get(path,{})
            else:
                cache = cache.get(path, {})
        if "city" in path_list:
            return self.schema.get_city_id_by_location_string(string)
        if "location" in path_list:
            return self.schema.get_city_id_by_location_string(string)
        return cache.get(string)