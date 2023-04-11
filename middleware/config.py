import os
import json
import aiohttp
import asyncio

from utils.custom_aiohttp_session import HoMuraSession


class Settings:

    # 转换服务-林雨森
    convert_server: str = os.getenv("CONVERT_SERVER", "http://localhost:9999")
    convert_url: str = convert_server + "/v2/converter"
    # 简历解析使用的转换id
    # parse_local_convert_task_id: str = os.getenv("PARSE_LOCAL_CONVERT_TASK_ID", "Resume:standard:2022_09_22_02_26_57")
    # parse_cloud_convert_task_id: str = os.getenv("PARSE_CLOUD_CONVERT_TASK_ID", "")

    # 简历解析-傅聪
    local_parse_server: str = os.getenv("PARSE_lOCAL_API_SERVER", "http://localhost:5050")
    local_parse_resume_url: str = local_parse_server + "/v5/file/parse/analyze"

    # 简历解析-外接api
    cloud_parse_appcode: str = os.getenv("CVPARSE_CLOUD_APPCODE", "085c11ede59c44588116918f0d3ee1ed")
    cloud_parse_server: str = os.getenv("PARSE_CLOUD_API_SERVER", "http://resumesdk.market.alicloudapi.com")
    cloud_parse_resume_url: str = cloud_parse_server + "/ResumeParser"

    # 简历解析-外接api-middleware
    cloud_parse_server_middleware: str = os.getenv("PARSE_CLOUD_MIDDLEWARE_API_SERVER", "http://localhost:5052")
    cloud_parse_file_middleware_url: str = cloud_parse_server_middleware + "/v5/file/parse/file-analyze"
    cloud_parse_b64_middleware_url: str = cloud_parse_server_middleware + "/v5/file/parse/b64-batch-analyze"

    # 简历解析fsg-middleware
    fsg_parse_server_middleware: str = os.getenv("PARSE_FSG_MIDDLEWARE_API_SERVER", "http://fsg-cvparser.nadileaf.com")
    fsg_parse_server_middleware_url: str = fsg_parse_server_middleware + "/files%3Aparse"


    # utils
    session: HoMuraSession = HoMuraSession(
        aiohttp.ClientSession, retry_interval=1, retry_when=lambda x: not isinstance(x, asyncio.exceptions.TimeoutError)
    )

    @classmethod
    def to_dict(cls):
        result = {}
        for key, value in cls.__annotations__.items():
            result[key] = getattr(cls, key).__str__()
        return result
    @classmethod
    def to_json(cls):
        result = {}
        for key, value in cls.__annotations__.items():
            result[key] = getattr(cls, key).__str__()
        return json.dumps(result, ensure_ascii=False, indent=2)

    @classmethod
    def initialize(cls):
        print("-" * 50 + "settings配置清单" + "-" * 50)
        print(cls.to_json())
