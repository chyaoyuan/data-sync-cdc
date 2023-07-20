from sqlalchemy import Table, Column, Integer, String, BigInteger, Date, DateTime, ForeignKey, func, JSON, BOOLEAN, LargeBinary, TEXT
from attachmentStorageServer.settings.settings import Settings
from attachmentStorageServer.database.base.application import Base


class AttachmentBaseInfoStorage(Base):
    """
    本体文件
    """
    __tablename__ = "base_info"
    id = Column(String(600), primary_key=True, index=True, comment="自增长")
    openId = Column(String(600), index=True, comment="自增长")
    tenant = Column(String(600), nullable=False, comment="租户")
    isDelete = Column(BOOLEAN, comment="软删除")
    createAt = Column(DateTime, server_default=func.now(), comment="创建时间")
    updateAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")

    # __mapper_args__ = {"order_by": email_receive_time.desc()}

    def __repr__(self):
        return f"{self.tenant} {self.entity} {self.tenant}"


attachment_info_table: Table = AttachmentBaseInfoStorage.__table__
attachment_info_table.metadata = Settings.DatabaseSettings.metadata
