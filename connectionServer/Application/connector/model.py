from pydantic import BaseModel, Field

from connectionServer.Application.config import DebeziumConfig


class ConfigInfo(BaseModel):
    # 详见 https://blog.csdn.net/Auspicious_air/article/details/123683033
    connector_class: str = Field(default=DebeziumConfig.connector_class, alias="connector.class")
    database_hostname: str = Field(default=DebeziumConfig.database_hostname, alias="database.hostname")
    database_port: str = Field(default=DebeziumConfig.database_port, alias="database.port")
    database_user: str = Field(default=DebeziumConfig.database_user, alias="database.user")
    database_password: str = Field(default="", alias="database.password")
    database_dbname: str = Field(default="", alias="database.dbname")
    database_server_name: str = Field(default="", alias="database.server.name", description="每个被监控的表在Kafka都会对应一个topic，topic的命名规范是<database.server.name>.<schema>.<table>")
    slot_name: str = Field(default="", alias="slot.name",description="PostgreSQL的复制槽(Replication Slot)名称")
    table_include_list: str = Field(default="", alias="table.include.list", description="如果设置,即在该list中的表才会被Debezium监控")
    publication_name: str = Field(default="", alias="publication.name")
    publication_auto_create_mode: str = Field(default="", alias="publication.autocreate.mode")
    plugin_name: str = Field(default="", alias="plugin.name")






class CreateConnector(BaseModel):
    name: str = Field(..., description="连接器名称")
    config: dict = Field(..., description="配置信息")


if __name__ == '__main__':
    i = ConfigInfo(**{
        "xx.xx":"xx"
    })
    print(i)