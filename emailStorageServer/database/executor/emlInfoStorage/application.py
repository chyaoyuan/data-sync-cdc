import asyncio

from loguru import logger
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import Insert

from emailStorageServer.database.base.application import Application
from emailStorageServer.data_model import GetEmailParams, PageParams

from emailStorageServer.database.executor.emlInfoStorage.model import EmailInfoInsertModel, GetEmailInfoParams, \
    GetEmailHtmlParams, GetEmailAttachmentsParams
from emailStorageServer.database_model import eml_info_table


class DataBaseIntegrate(Application):
    table = eml_info_table
    select_params = ["emailUniqueId", "sender", "receiver", "subject", "receiveTime"]

    async def upsert_email_info(self, email_info: dict):
        """
        更新插入邮件
        """
        email_info = EmailInfoInsertModel(**email_info)
        insert_sql: Insert = Insert(eml_info_table, inline=True).values(email_info.dict())
        insert_sql = insert_sql.on_conflict_do_update(
            index_elements=['id'],
            set_=email_info.dict()
        )
        db = await self.get_db()
        await db.execute(insert_sql)
        logger.info(f"存入邮件Info成功 tenant->{email_info.tenant} uid->{email_info.id} subject->{email_info.subject} time->{email_info.receiveTime}")
        return True

    # async def GetEmailInfoByUID(self, email_search_params: dict):
    #     """
    #     查询单封邮件基础信息(不含大文件)
    #     """
    #     params = GetEmailInfoParams(**email_search_params).dict()
    #     query = select([eml_info_table.c[sp] for sp in cls.select_params]).filter_by(**params)
    #     result = await db.fetch_one(query)
    #     return dict(result) if result else {}

    # @classmethod
    # @connection_wrapper
    # async def SearchEmailInfo(cls, email_search_params: dict):
    #     """
    #     混合条件查询单封邮件基础信息(不含大文件)
    #     """
    #     params = GetEmailParams(**email_search_params).dict()
    #     params = {key: value for key, value in params.items()if value}
    #     query = select([eml_info_table.c[sp] for sp in cls.select_params]).filter_by(**params)
    #     result = await db.fetch_one(query)
    #     return dict(result) if result else {}
    #
    # @classmethod
    # @connection_wrapper
    # async def SearchEmailsInfo(cls, email_search_params: dict, page_params: dict):
    #     """
    #     查询多封邮件基础信息(不含大文件)
    #     """
    #     params = GetEmailParams(**email_search_params).dict()
    #     params = {key: value for key, value in params.items() if value}
    #     page_params = PageParams(**page_params)
    #     query = select([eml_info_table.c[sp] for sp in cls.select_params]).filter_by(**params).order_by(eml_info_table.c.receiveTime.desc()).limit(page_params.pageSize).offset(page_params.pageSize*(page_params.pageIndex-1))
    #     results = await db.fetch_all(query)
    #     return [dict(result) for result in results] if results else None
    #
    # @classmethod
    # @connection_wrapper
    # async def GetEmailAttachments(cls, email_search_params: dict):
    #     """
    #     查询单封邮件附件
    #     """
    #     params = GetEmailAttachmentsParams(**email_search_params).dict()
    #     query = eml_info_table.select().filter_by(**params).order_by(eml_info_table.c.receiveTime.desc())
    #     result = await db.fetch_one(query)
    #     return dict(result) if result else None
    #
    # @classmethod
    # @connection_wrapper
    # async def GetEmailHtml(cls, email_search_params: dict):
    #     """
    #     查询单封邮件html
    #     """
    #     params = GetEmailHtmlParams(**email_search_params).dict()
    #     query = eml_info_table.select().filter_by(**params).order_by(
    #         eml_info_table.c.receiveTime.desc())
    #     result = await db.fetch_one(query)
    #     return dict(result) if result else {}


if __name__ == '__main__':
    pass
    # body = {
    #     "id": "c135487755afdf5ba154a8d2c4b6ff0c",
    # }
    # i = asyncio.run(DataBaseIntegrate.SearchEmailInfo(body))
    # print(i)

    body = {
        "tenant": "tenant",
    }
    i = asyncio.run(DataBaseIntegrate.SearchEmailsInfo(body))
    print(i)

    # body = {
    #     "emailUniqueId": "c135487755afdf5ba154a8d2c4b6ff0c"
    # }
    # i = asyncio.run(DataBaseIntegrate.GetEmailHtml(body))

    # body = {
    #     "emailUniqueId": "c135487755afdf5ba154a8d2c4b6ff0c"
    # }
    # i = asyncio.run(DataBaseIntegrate.GetEmailBody(body))
    # i = i['body']
    #
    # i = [base64.b64decode(line).decode(encoding='UTF-8') for line in i]
    # x = "\n".join(i)
    # with open("xx.eml", "wb") as f:
    #     f.write(x.encode())


    logger.info(i)