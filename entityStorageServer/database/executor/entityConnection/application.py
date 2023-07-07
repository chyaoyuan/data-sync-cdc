from loguru import logger
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import Insert
from entityStorageServer.database.base.application import Application
from entityStorageServer.database.executor.entity.model import EntityInsertModel
from entityStorageServer.database.table.tabel_model import entity_info_table


class EntityConnectionDataBaseIntegrate(Application):
    table = entity_info_table

    async def create_entity_connection(self, body: dict):
        _body = EntityInsertModel(**body)
        insert_sql: Insert = Insert(self.table, inline=True).values(_body.dict())
        insert_sql = insert_sql.on_conflict_do_update(
            index_elements=['id'],
            set_=_body.dict()
        )
        db = await self.get_db()
        await db.execute(insert_sql)
        logger.info(f"存入实体成功 tenant->{_body.tenant} entity->{_body.entity_type} uid->{_body.source_id}")

    async def get_entity(self, body: dict):

        params = EntityInsertModel(**body).dict()
        query = select([self.table.c["payload"]]).filter_by(**params)
        return await self.fetch_one(query)


