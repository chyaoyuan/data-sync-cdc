from typing import Type

from entityStorageServer.database.executor.entity.application import DataBaseIntegrate
from entityStorageServer.settings.settings import Settings
from entityStorageServer.database.base.application import Base


class Application:
    def __init__(self, settings: Type[Settings]):
        self.settings = settings
        self.entity_info = DataBaseIntegrate(self.settings)

    @staticmethod
    def init_tables():
        Base.metadata.create_all()


database_app = Application(Settings)



