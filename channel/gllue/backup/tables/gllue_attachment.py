import sqlalchemy
from sqlalchemy.sql.functions import func

from channel.gllue.config import Settings
from channel.gllue.database.base.application import Base


class Table(Base):
    __tablename__ = 'gllue-attachment'
    id = sqlalchemy.Column(sqlalchemy.String(600), primary_key=True)
    tenant = sqlalchemy.Column(sqlalchemy.String(600), index=True)
    openid = sqlalchemy.Column(sqlalchemy.String(600))
    entityType = sqlalchemy.Column(sqlalchemy.String(600), nullable=False)
    fileName = sqlalchemy.Column(sqlalchemy.String(600), nullable=True)
    payload = sqlalchemy.Column(sqlalchemy.LargeBinary, nullable=False)
    createTime = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, server_default=func.now())
    updateTime = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, index=True,
                                   server_default=func.now(), onupdate=func.now())


table: sqlalchemy.Table = Table.__table__
table.metadata = Settings.DatabaseSettings.metadata
