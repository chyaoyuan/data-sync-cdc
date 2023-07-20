
from middleware.entityStorage.entity.application import EntityApplication
from middleware.settings.settings import Settings



class EntityStorageMiddleware:
    def __init__(self):
        self.entity_storage_app = EntityApplication(Settings)
