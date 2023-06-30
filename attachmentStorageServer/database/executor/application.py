from typing import Type

from attachmentStorageServer.database.table.tabel_model import attachment_info_table
from emailStorageServer.config import Settings

from emailStorageServer.database.base.application import Base


class Application:
    def __init__(self, settings: Type[Settings]):
        self.settings = settings
        self.attachment_info = attachment_info_table

    @staticmethod
    def init_tables():
        Base.metadata.create_all()


application = Application(Settings)



