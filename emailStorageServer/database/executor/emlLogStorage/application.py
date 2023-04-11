import asyncio
import base64

import databases
from functools import wraps
from loguru import logger
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import Insert
from config import DatabaseSettings
from typing import Callable, Optional

from database_integrate.base.application import connection_wrapper, db
from database_integrate.eml_logger_storage.model import EmailLogInsertModel
from database_model import eml_log_table
from pyd_model import EmailModel, GetEmailParams, GetEmailAttachmentsParams, GetEmailHtmlParams, EmailStatusModel, \
    PageParams


class DataBaseIntegrate:
    select_params = ["emailUniqueId", "tenant", "channel", "sender", "receiver", "subject", "receiveTime", "retryCount", "candidateId", "location", "position", "source"]
    _select_params = ["retryCount", "isDelete"]

    @classmethod
    @connection_wrapper
    async def UpsertEmailLog(cls, email_info: dict):
        """
        更新插入邮件日志
        """
        email_info = EmailLogInsertModel(**email_info)
        insert_sql: Insert = Insert(eml_log_table, inline=True).values(email_info.dict())
        insert_sql = insert_sql.on_conflict_do_update(
            index_elements=['id'],
            set_=email_info.dict()
        )
        await db.execute(insert_sql)
        return True

    @classmethod
    @connection_wrapper
    async def SearchEmailsStatus(cls, email_search_params: dict) -> Optional[EmailStatusModel]:
        """
        查询单封邮件状态信息(isDelete 和 retry)
        """
        result = await cls._SearchEmailsStatus(email_search_params)
        return EmailStatusModel(**email_search_params) if result else None


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