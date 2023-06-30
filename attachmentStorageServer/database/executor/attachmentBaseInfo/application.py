from loguru import logger
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import Insert

from attachmentStorageServer.database.base.application import Application
from attachmentStorageServer.database.executor.attachmentBaseInfo.model import AttachmentBodyInsertModel, \
    SearchAttachmentModel
from attachmentStorageServer.database.table.tabel_model import attachment_info_table


class DataBaseIntegrate(Application):
    table = attachment_info_table

    async def update_attachment_info_body(self, body: dict):
        _body = AttachmentBodyInsertModel(**body)
        insert_sql: Insert = Insert(self.table, inline=True).values(_body.dict())
        insert_sql = insert_sql.on_conflict_do_update(
            index_elements=['id'],
            set_=_body.dict()
        )
        db = await self.get_db()
        await db.execute(insert_sql)
        logger.info(f"存入附件成功 tenant->{_body.tenant} uid->{_body.openId}")

    async def get_attachment_info_body(self, body: dict):

        params = SearchAttachmentModel(**body).dict()
        query = select([self.table.c["body"]]).filter_by(**params)
        return await self.fetch_one(query)


if __name__ == '__main__':
    pass
