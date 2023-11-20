import json
import os

from loguru import logger


class FileSettings:
    tenant_list = os.getenv("TenantList", "waifu").split(",")
    BASE_DIR = os.getenv('BASE_DIR', os.path.join(os.path.dirname(__file__), "data"))
    flow_config = {}
    for tenant in tenant_list:
        with open(os.path.join(BASE_DIR, f"{tenant}_flow_config.json")) as f:
            flows = json.loads(f.read())
            logger.info(f"加载租户Flow配置->{tenant}")
        flow_config[tenant] = flows


class GleUserConfig:
    env_field_name_list = ["ApiServerHost", "AesKey", "Account"]
    # 去掉_为真参数
    env_field_default_list = ["https://fsgtest.gllue.net", "824531e8cad2a287", "api@fsg.com.cn"]
    env_var = {}
    for _env_name, _default in zip(env_field_name_list, env_field_default_list):
        env_var[_env_name[0].lower()+_env_name[1:]] = os.getenv(_env_name, _default)


class SyncConfig:
    env_field_name_list = ["EntityName", "Recent", "Unit", "OrderBy", "SyncModel", "TimeFieldName", "syncAttachment"]
    env_field_default_list = ["jobOrder", "3", "day", "-id", "Recent", "lastUpdateDate__day_range", True]
    env_var = {}
    for _env_name, _default in zip(env_field_name_list, env_field_default_list):
        env_var[_env_name[0].lower()+_env_name[1:]] = os.getenv(_env_name, _default)


class SyncConfigGql:
    env_field_name_list = ["EntityName", "gql", "OrderBy", "SyncModel", "syncAttachment"]
    env_field_default_list = ["candidate", "id__s=574",  "-id", "Recent", True]
    env_var = {}
    for _env_name, _default in zip(env_field_name_list, env_field_default_list):
        env_var[_env_name[0].lower()+_env_name[1:]] = os.getenv(_env_name, _default)


class ExtraConfig:
    time_sleep = int(os.getenv("SleepTimes", "180"))


class TipConfig:
    tenant_alias = os.getenv("TenantAlias", "waifu")


class TipMiddlewareConfig:
    settings = {
        "entityStorageServerHost": os.getenv("EntityStorageServerHost", "http://localhost:9400"),
        "TipTagServerHost": os.getenv("TipTagServerHost", "http://effex.tpddns.cn:7777")}


class Settings:
    FileSettings = FileSettings
    ExtraConfig = ExtraConfig
    TipConfig = TipConfig
    TipMiddlewareConfig = TipMiddlewareConfig
    GleUserConfig: dict = GleUserConfig.env_var
    SyncConfig: dict = SyncConfig.env_var
    SyncConfigGql: dict = SyncConfigGql.env_var






