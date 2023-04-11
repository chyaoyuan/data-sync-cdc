from enum import Enum


class Entity(Enum):
    Candidate = "Candidate"
    Position = "Position"


class GleSchemaUrl:
    def __init__(self, typeName: str, apiServerHost: str):
        # 获取所有字段
        self.get_schema: str = "{apiServerHost}/rest/custom_field/{typeName}".format(typeName=typeName,apiServerHost=apiServerHost)