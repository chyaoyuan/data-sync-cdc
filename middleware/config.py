import os
import json
import aiohttp
import asyncio

from utils.custom_aiohttp_session import HoMuraSession


class Settings:
    store_derivation_server: str = os.getenv("STORE_DERIVATION_SERVER", "http://localhost:9200")
    resume_parser_server: str = os.getenv("CVPARSER_API_SERVER", "http://localhost:5050")
    # http://airflow-controller-server-dev.airflow-dev.svc.cluster.local
    # airflow_controller_server: str = os.getenv(
    #     "AIRFLOW_CONTROLLER_SERVER", "http://localhost:12000"
    # )
    airflow_controller_server: str = os.getenv(
        "AIRFLOW_CONTROLLER_SERVER", "https://data-sync.mesoor.com/api/airflow-controller"
    )
    # transmitter_v2_server: str = os.getenv("TRANSMITTER_V2_SERVER", "https://transmitter.nadileaf.com/v2/entity")
    transmitter_v2_server: str = os.getenv("TRANSMITTER_V2_SERVER", "https://ruleengine.nadileaf.com")
    rule_engine_server: str = os.getenv("RULE_ENGINE_SERVER", "http://localhost:57978")
    # rule_engine_server: str = os.getenv("RULE_ENGINE_SERVER", "https://ruleengine.nadileaf.com")
    transmitter_schema_server: str = os.getenv("TRANSMITTER_SCHEMA_SERVER", "https://transmitter-schema.nadileaf.com")
    max_transmitter_entity_size: int = int(os.getenv("MAX_TRANSMITTER_ENTITY_SIZE", "262144"))
    newest_schema_url: str = transmitter_schema_server + "/v2/publish/entity/{tenant}/{entityType}/publishLink"
    transmitter_v2_save_entity_url: str = rule_engine_server + "/v2/entity/{tenant}/{entityType}/{entityId}"
    transmitter_v2_get_entity_url: str = transmitter_v2_server + "/v2/entity/{tenant}/{entityType}/{entityId}"
    transmitter_v2_delete_entity_url: str = transmitter_v2_server + "/{tenant}/{entityType}/{entityId}"
    transmitter_editor: str = "woshidashuaibi"
    convert_server: str = os.getenv("CONVERT_SERVER", "http://localhost:9999")
    airflow_trigger_dag_run_url: str = airflow_controller_server + "/dagRun/trigger"
    airflow_upsert_pool_url: str = airflow_controller_server + "/pool/save"
    save_channel_url: str = store_derivation_server + "/store/channel/save"
    save_project_url: str = store_derivation_server + "/store/project/save"
    save_project_stage_url: str = store_derivation_server + "/store/project/flowStage/save"
    save_file_url: str = store_derivation_server + "/store/file/save"
    save_b64_file_url: str = store_derivation_server + "/store/file/save/base64"
    move_flow_url: str = store_derivation_server + "/store/flows/add"
    save_entity_custom_fields_url: str = store_derivation_server + "/store/entity/customFields/save"
    convert_url: str = convert_server + "/v2/converter"
    internal_schema_info_url: str = convert_server + "/v2/internal_schema/list"
    resume_parser_url: str = resume_parser_server + "/v5/file/parse/analyze"
    session: HoMuraSession = HoMuraSession(
        aiohttp.ClientSession, retry_interval=1, retry_when=lambda x: not isinstance(x, asyncio.exceptions.TimeoutError)
    )

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
