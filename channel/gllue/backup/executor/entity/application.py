import asyncio
from loguru import logger
from sqlalchemy import select
from sqlalchemy.dialects.postgresql.dml import Insert

from channel.gllue.config import Settings
from channel.gllue.database.base.application import Application as BaseApplication
from channel.gllue.database.executor.entity.model import EntityModel
from channel.gllue.database.tables.gllue_entity import table as gle_entity


class Application(BaseApplication):
    table = gle_entity

    # async def get_entity_by_tenant(self, tenant: str):
    #     "获取config"
    #     query = self.table.select().filter_by(**{"id": tenant, "isDelete": False})
    #     result = await self.fetch_one(query)
    #     logger.info(f"获取配置成功->{tenant} {result}")
    #     return result
    #
    async def get_all_ids_by_tenant(self, tenant: str, entityType: str):
        "根据tenant、entityType获取所有openID"
        query = select(self.table.c["id"]).filter_by(tenant=tenant, entityType=entityType).order_by(self.table.c.updateTime)
        result = await self.fetch_all(query)
        return [_id["id"] for _id in result]

    async def put_entity(self, body: dict):
        "不管不顾直接复写"
        entity = EntityModel(**body)
        insert_sql: Insert = Insert(self.table, inline=True).values(entity.dict())
        insert_sql = insert_sql.on_conflict_do_update(
            index_elements=["id"], set_=entity.dict()
        )
        db = await self.get_db()
        await db.execute(insert_sql)
        logger.info(f"put entity success->{entity.id} {entity.dict()}")

    async def get_entity_by_unique_id(self, unique_id: str):
        "根据id获取实体"
        query = select(self.table).filter_by(id=unique_id)
        return await self.fetch_one(query)



if __name__ == '__main__':
    app = Application(Settings)
    pass
    # 不管不顾直接更新
    i = {'id': 30, 'openId': 'Gllue-Job-5jlh62781a6zw-30', 'payload': {'_approval_status': None, 'jobTitle': '人工智能大会WAIC-现场组实习生', 'annualSalary': None, 'lastUpdateBy': 4, 'id': 30, 'dateAdded': '2023-02-15 10:51:24', 'is_deleted': False, 'addedBy': 4, 'lastUpdateDate': '2023-02-15 10:57:19', 'lastContactBy': None, 'lastContactDate': None, '__name__': '人工智能大会WAIC-现场组实习生', 'jobsubmission_count': {'name': 8, 'link': '#joborder/detail?id=30'}, 'accessSource': 'EDIT ALL', 'accessLevel': 'FullAccess'}, 'tenant': '5jlh62781a6zw', 'entityType': 'Job'}



    # 软删除
    exe = app.put_entity(i)

    # exe = app.get_config_id(tenant="mesoor-98")
    asyncio.run(exe)

