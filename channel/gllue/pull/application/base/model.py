from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class GleUrlConfig:
    # 谷露的接口定义
    get_entity_url = "/rest/{entityType}/simple_list_with_ids"
    get_entity_schema_url = "/rest/custom_field/{entityType}"
    # 系统参数的数据字典(来自文档)
    get_system_model_url = "/rest/custom_field/{entityType}/list"
    # 参数字典(来自前端)
    get_field_schema_url = "/rest/{entityType}/list"


class BaseResponseModel(BaseModel):
    # 谷露的请求成功的标准返回值格式
    ids: list = Field(..., description="ID列表")
    currentpage: int = Field(..., description="当前页码")
    totalcount: int = Field(..., description="rows总量")
    totalpages: int = Field(..., description="总页数")
    result: Optional[dict]
    # 谷露的请求失败的标准返回值格式
    message: Optional[str] = Field(default=None, description="错误信息")




# class GleURL:
#     def __init__(self, apiServerHost: str):
#         # 一般用于测试token有效性
#         self.candidate_simple_list_with_ids_url: str = "{apiServerHost}/rest/candidate/simple_list_with_ids".format(apiServerHost=apiServerHost)
#         self.check = "{apiServerHost}/rest/joborder/simple_list_with_ids".format(apiServerHost=apiServerHost)
