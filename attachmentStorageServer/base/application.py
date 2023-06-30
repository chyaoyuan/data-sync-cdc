from typing import Type
from attachmentStorageServer.settings.settings import Settings


class Application:
    def __init__(self, settings: Type[Settings]):
        self.settings = settings
