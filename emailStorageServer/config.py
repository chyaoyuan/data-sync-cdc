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
    pg_database: str = os.getenv('POSTGRES_DB', 'data-sync-storage')
    db_schema: Optional[str] = os.getenv("DB_SCHEMA")
    database_url: str = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"

    engine, metadata = get_engine_and_metadata(database_url, schema=db_schema)
    db_instance: databases.Database = databases.Database(database_url)


class Settings:
    DatabaseSettings = DatabaseSettings
    eml_app_server_host: str = os.getenv("EMAIL_APP_SERVER", "localhost:8091")
    eml_decode_url: str = f"http://{eml_app_server_host}/v1/emailApplication/Decode/body"
