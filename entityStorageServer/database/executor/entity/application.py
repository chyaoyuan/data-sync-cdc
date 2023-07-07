from loguru import logger
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import Insert

from entityStorageServer.database.base.application import Application
from entityStorageServer.database.executor.entity.model import EntityInsertModel, SearchEntityModel
from entityStorageServer.database.table.tabel_model import entity_info_table


class DataBaseIntegrate(Application):
    table = entity_info_table

    async def put_entity(self, body: dict):
        body["is_delete"] = False
        _body = EntityInsertModel(**body)
        insert_sql: Insert = Insert(self.table, inline=True).values(_body.dict())
        insert_sql = insert_sql.on_conflict_do_update(
            index_elements=['tenant', 'entity_type', 'source_id'],
            set_=_body.dict()
        )
        db = await self.get_db()
        await db.execute(insert_sql)
        logger.info(f"存入实体成功 tenant->{_body.tenant} entity->{_body.entity_type} uid->{_body.source_id}")

    async def get_entity(self, body: dict):
        body["is_delete"] = False
        params = SearchEntityModel(**body).dict()
        query = select([self.table.c["payload"]]).filter_by(**params)
        return await self.fetch_one(query)


if __name__ == '__main__':
    pass
