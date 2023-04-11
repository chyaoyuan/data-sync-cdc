import os


class PostgresConfig:
    DATABASE_HOST_NAME: str = os.getenv("DATABASE_HOST_NAME", "postgres")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT", "5432")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "postgres")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "postgres")
    DATABASE_DBNAME: str = os.getenv("DATABASE_DBNAME","data-sync-cdc")


class DebeziumConfig:
    connector_class = "io.debezium.connector.postgresql.PostgresConnector",
    database_hostname: str = PostgresConfig.DATABASE_HOST_NAME
    database_port: str = PostgresConfig.DATABASE_PORT
    database_user: str = PostgresConfig.DATABASE_USER
    database_password: str = PostgresConfig.DATABASE_PASSWORD
    database_dbname: str = PostgresConfig.DATABASE_DBNAME
    database_server_name: str = "debezium",
    slot_name: str = "inventory_slot",
    table_include_list: str = "inventory.orders,inventory.products",
    publication_name: str = "dbz_inventory_connector",
    publication_auto_create_mode:  str = "filtered",
    plugin_name: str = "pgoutput"


class Settings:
    DEBEZIUM_CON_HOST: str = os.getenv("DEBEZIUM_CON_HOST", "")
    DEBEZIUM_CON_CONNECTOR: str = f"{DEBEZIUM_CON_HOST}/connectors"
