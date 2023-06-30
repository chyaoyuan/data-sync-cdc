from typing import Any, List, Optional
from attachmentStorageServer.base.application import Application as BaseApplication


class Application(BaseApplication):
    async def get_db(self):
        if not self.settings.DatabaseSettings.db_instance.is_connected:
            await self.settings.DatabaseSettings.db_instance.connect()
        return self.settings.DatabaseSettings.db_instance

    async def fetch_all(self, query: Any) -> List[dict]:
        db = await self.get_db()
        result: list = await db.fetch_all(query)
        return list(map(dict, result))

    async def fetch_one(self, query: Any) -> Optional[dict]:
        db = await self.get_db()
        result = await db.fetch_one(query)
        return dict(result) if result is not None else None

    async def session_(self, query: Any) -> Optional[dict]:
        db = await self.get_db()
        result = await db.fetch_one(query)
        return dict(result) if result is not None else None