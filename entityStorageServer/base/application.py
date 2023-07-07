from typing import Type
from entityStorageServer.settings.settings import Settings


class Application:
    def __init__(self, settings: Type[Settings]):
        self.settings = settings
