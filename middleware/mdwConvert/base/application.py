from typing import Type
from middleware.config import Settings


class Application:
    def __init__(self, settings: Type[Settings]):
        self.settings = settings
