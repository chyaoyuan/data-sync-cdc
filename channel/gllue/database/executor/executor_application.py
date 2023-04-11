from typing import Type

from channel.gllue.config import Settings
from channel.gllue.database.base.application import Base

from channel.gllue.database.executor.entity.application import Application as EntityApplication


class DataBaseExecutorApplication:


    def __init__(self, settings: Type[Settings]):
        self.settings = settings
        self.entity = EntityApplication(self.settings)

    @staticmethod
    def init_tables():
        Base.metadata.create_all()


application = DataBaseExecutorApplication(Settings)
app = application.entity

