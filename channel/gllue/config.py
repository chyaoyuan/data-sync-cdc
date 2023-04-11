import json
import os
from typing import Optional
import databases
import sqlalchemy
from loguru import logger
from sqlalchemy_utils import database_exists, create_database


def get_engine(url: str):
    return sqlalchemy.create_engine(url)


def get_metadata(engine: sqlalchemy.engine.Engine, *, schema: Optional[str] = None):
    if schema is not None:
        metadata = sqlalchemy.MetaData(schema=schema)
    else:
        metadata = sqlalchemy.MetaData()
    metadata.bind = engine


def get_engine_and_metadata(url: str, *, schema: Optional[str] = None):
    if not database_exists(url):
        create_database(url)
        logger.info("创建 {} 成功".format(url))
    else:
        logger.info("{} 存在".format(url))
    engine = get_engine(url)
    return engine, get_metadata(engine, schema=schema)


class DatabaseSettings:
    pg_user: str = os.getenv('POSTGRES_USER', 'postgres')
    pg_password: str = os.getenv('POSTGRES_PASSWORD', 'postgres')
    pg_host: str = os.getenv('POSTGRES_HOST', 'localhost')
    pg_port: str = int(os.getenv('POSTGRES_PORT', '5432'))
    pg_database: str = os.getenv('POSTGRES_DB', 'data-sync')
    db_schema: Optional[str] = os.getenv("DB_SCHEMA")
    database_url: str = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"

    engine, metadata = get_engine_and_metadata(database_url, schema=db_schema)
    db_instance: databases.Database = databases.Database(database_url)


class Settings:
    DatabaseSettings = DatabaseSettings
    # document
    document_path = os.getenv("DOCUMENT_PATH", "/docs")
    model: bool = bool(os.getenv("MODEL", False))

    forward: str = os.getenv("FORWARD", "local")

    forwardSettings: list = [
     {
          "name": "cvpLocal",
          "description": "傅聪的简历解析",
          "convertConfig": [
               {
                    "tag": "chinese",
                    "taskId": "Resume:standard:2022_09_22_02_26_57"
               }
          ]
     },
     {
          "name": "cvpCloud",
          "description": "ResumeSDK的简历解析",
          "url": "http://cvparse-cloud-server/v5/file/parse/b64-batch-analyze",
          "convertConfig": [
               {
                    "tag": "chinese",
                    "taskId": "Resume:standard:2023_03_16_09_09_56"
               }
          ]
     },
     {
          "name": "cvpFSG",
          "description": "zxg的简历解析",
          "url": "https://fsg-cv-parser.nadileaf.com/files%3Aparse",
          "convertConfig": [
               {
                    "tag": "chinese",
                    "taskId": "Resume:standard:2023_03_16_09_09_56"
               }
          ]
     }
]

    @classmethod
    def to_dict(cls) -> dict:
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