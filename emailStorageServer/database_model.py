import sqlalchemy
from loguru import logger
from sqlalchemy import create_engine, MetaData, Index
from sqlalchemy import Table, Column, Integer, String, BigInteger, Date, DateTime, ForeignKey, func, JSON, BOOLEAN, LargeBinary, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from emailStorageServer.config import DatabaseSettings, Settings

engine = create_engine(DatabaseSettings.database_url, encoding="utf-8", echo=True)
session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=True)
from emailStorageServer.database.base.application import Base


class EmailBodyStorage(Base):
    """
    邮件本体文件
    """
    __tablename__ = "emailBody"
    id = Column(String(600), primary_key=True, comment="邮件唯一ID含租户参数")
    body = Column(JSON, nullable=False, comment="邮件本体")
    tenant = Column(String(600), nullable=False, comment="租户")
    createAt = Column(DateTime, server_default=func.now(), comment="创建时间")
    updateAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")

    # __mapper_args__ = {"order_by": email_receive_time.desc()}

    def __repr__(self):
        return f"{self.id} {self.tenant} {self.channel} {self.email_receive_time} {self.subject}"


class EmailInfoStorage(Base):
    """
    邮件本体详情
    """
    __tablename__ = "emailInfo"
    id = Column(String(600), primary_key=True, comment="邮件唯一ID含租户参数")
    emailUniqueId = Column(String(600), nullable=False, comment="邮件唯一ID含租户参数")
    sender = Column(String(600), nullable=False, comment="发件人邮箱")
    receiver = Column(String(600), nullable=False, comment="收件人邮箱")
    subject = Column(String(600), nullable=False, comment="邮件主题")
    html = Column(TEXT, nullable=False, comment="邮件正文")
    receiveTime = Column(DateTime, nullable=False, comment="邮件时间")
    attachments = Column(JSON, comment="附件列表")
    tenant = Column(String(600), nullable=False, comment="租户")
    fileName = Column(String(600), nullable=False, comment="文件名")
    extra = Column(JSON, nullable=True, comment="额外字段")
    source = Column(String(600), nullable=False, comment="来源")
    candidateId = Column(JSON, nullable=False, comment="候选人ID，自定义邮件会出现一封邮件多个候选人的情况 ")
    location = Column(String(600), nullable=True, comment="地点")
    position = Column(String(600), nullable=True, comment="职位名")
    candidateUrl = Column(String(600), nullable=True, comment="候选人链接")
    channel = Column(String(600), nullable=False, comment="邮件渠道")
    isDelete = Column(BOOLEAN, nullable=True, comment="软删除")
    createAt = Column(DateTime, server_default=func.now(), comment="创建时间")
    updateAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")

    __table_args__ = (
        Index('idx_tenant_createAt', 'tenant', 'createAt'),
        Index('idx_tenant_receiveTime', 'tenant', 'receiveTime'),
        Index('idx_tenant_updateAt', 'tenant', 'updateAt'),
    )


class EmailLogStorage(Base):
    """
    邮件运行日志
    """
    __tablename__ = "emailLogInfo"
    id = Column(String(600), primary_key=True, comment="邮件唯一ID含租户参数")
    autoRetryCount = Column(Integer, nullable=False, comment="自动化任务触发重试次数")
    manualRetryCount = Column(Integer, nullable=False, comment="手动触发重试次数")
    retrySignal = Column(BOOLEAN, nullable=False, comment="是否重试")
    retryExtra = Column(JSON, nullable=True, comment="额外字段")
    createAt = Column(DateTime, server_default=func.now(), comment="创建时间")
    updateAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")

    __table_args__ = (
        Index('idx_tenant_updateAt', 'tenant', 'updateAt'),
    )


# 汇总了三张表

eml_body_table: Table = EmailBodyStorage.__table__
eml_body_table.metadata = Settings.DatabaseSettings.metadata
eml_info_table: Table = EmailInfoStorage.__table__
eml_info_table.metadata = Settings.DatabaseSettings.metadata
eml_log_table: Table = EmailLogStorage.__table__
eml_info_table.metadata = Settings.DatabaseSettings.metadata