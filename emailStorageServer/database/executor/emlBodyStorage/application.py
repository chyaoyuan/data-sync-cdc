from loguru import logger
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import Insert

from emailStorageServer.database.base.application import Application
from emailStorageServer.database.executor.emlBodyStorage.model import EmailBodyInsertModel, EmailBodyDownloadModel
from emailStorageServer.database_model import eml_body_table


class DataBaseIntegrate(Application):
    table = eml_body_table

    async def upsert_email_body(self, email_info: dict):
        """
        更新插入邮件body
        """
        email_info = EmailBodyInsertModel(**email_info)
        insert_sql: Insert = Insert(self.table, inline=True).values(email_info.dict())
        insert_sql = insert_sql.on_conflict_do_update(
            index_elements=['id'],
            set_=email_info.dict()
        )
        db = await self.get_db()
        await db.execute(insert_sql)
        logger.info(f"存入邮件Body成功 tenant->{email_info.tenant} uid->{email_info.id}")

    async def get_email_body(self, email_search_params: dict):
        """
        下载单封邮件body
        """
        params = EmailBodyDownloadModel(**email_search_params).dict()
        query = select([self.table.c["body"]]).filter_by(**params)
        return await self.fetch_one(query)


if __name__ == '__main__':
    pass
