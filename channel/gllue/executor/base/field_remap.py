import json
import os
from loguru import logger
from channel.gllue.executor.config.settings import Settings


def config_map(_config: dict):
    logger.info(_config)
    tenant_alias = _config.pop("tenantAlias")
    primary_entity_name = _config["primaryEntityName"]
    extra_entity_name_list: list = _config.get("extraEntityName", [])
    BASE_DIR = os.getenv('BASE_DIR', os.path.join(os.path.dirname(__file__), "../config/tenantConfig"))
    with open(os.path.join(BASE_DIR, f"{tenant_alias}.json")) as f:
    # with open(f"../config/tenantConfig/{tenant_alias}.json") as f:
        base_config = json.loads(f.read())
    assert base_config["tenantAlias"] == tenant_alias
    primary_entity_config = base_config["syncFlow"][primary_entity_name.value]

    extra_entity_config: list = [base_config["syncFlow"][_name] for _name in extra_entity_name_list]

    # 谷露用户配置
    gle_user_config = {
        "apiServerHost": _config.pop("apiServerHost"),
        "aesKey": _config.pop("aesKey"),
        "account": _config.pop("account"),
    }
    # 同步flow配置
    new_config = {
        **_config,
        **primary_entity_config,
        "extraEntity": extra_entity_config
    }
    # 数据获取模式配置
    sync_model = {"syncModel": new_config["syncModel"]}
    # Tip配置
    tip_config = {"tenantAlias": tenant_alias}
    return gle_user_config, sync_model, new_config, tip_config
