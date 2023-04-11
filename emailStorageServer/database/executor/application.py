from typing import Type

from emailStorageServer.config import Settings
from emailStorageServer.database.executor.emlBodyStorage.application import DataBaseIntegrate as EmlBodyApp
from emailStorageServer.database.executor.emlInfoStorage.application import DataBaseIntegrate as EmlInfoApp
from emailStorageServer.database.base.application import Base


class Application:
    def __init__(self, settings: Type[Settings]):
        self.settings = settings
        self.email_body_app = EmlBodyApp(self.settings)
        self.email_info_app = EmlInfoApp(self.settings)

    @staticmethod
    def init_tables():
        Base.metadata.create_all()


application = Application(Settings)



