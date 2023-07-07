from sqlalchemy import Table, Column, Integer, String, BigInteger, Date, DateTime, ForeignKey, func, JSON, BOOLEAN, \
    LargeBinary, TEXT, UniqueConstraint, Index
from entityStorageServer.settings.settings import Settings
from entityStorageServer.database.base.application import Base


class EntityInfoStorage(Base):
    __tablename__ = "entity"
    id = Column(Integer, primary_key=True,autoincrement=True, comment="自增长")
    entity_type = Column(String(600), nullable=False, comment="实体名称")
    source_id = Column(String(600), index=True, nullable=False, comment="自增长")
    tenant = Column(String(600), nullable=False, comment="租户")
    payload = Column(JSON, nullable=False, comment="实体内容")
    is_delete = Column(BOOLEAN, nullable=False, comment="软删除")
    create_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    update_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")

    # __mapper_args__ = {"order_by": email_receive_time.desc()}

    __table_args__ = (
        UniqueConstraint('tenant', 'entity_type', 'source_id', name='uk_index'),
        Index('idx_uk_index', 'tenant', 'entity_type', 'source_id'),
    )

    def __repr__(self):
        return f"{self.tenant} {self.entity} {self.tenant}"


class EntityConnectionStorage(Base):
    __tablename__ = "entity_connection"
    id = Column(String(600), primary_key=True, index=True, comment="自增长")
    ms_entity_type = Column(String(600), nullable=False, comment="麦穗实体名称")
    open_id = Column(String(600), primary_key=True, index=True, comment="自增长")
    tenant = Column(String(600), nullable=False, comment="租户")
    # entity 表里的ID
    entity_id = Column(JSON, nullable=False, comment="实体内容")
    is_delete = Column(BOOLEAN, comment="软删除")
    create_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    update_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")

    # __mapper_args__ = {"order_by": email_receive_time.desc()}

    def __repr__(self):
        return f"{self.tenant} {self.entity} {self.tenant}"


entity_info_table: Table = EntityInfoStorage.__table__
entity_info_table.metadata = Settings.DatabaseSettings.metadata

entity_connection_table: Table = EntityConnectionStorage.__table__
entity_connection_table.metadata = Settings.DatabaseSettings.metadata