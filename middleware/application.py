from middleware.entityStorage.application import EntityStorageMiddleware
from middleware.tagging.application import TagMiddleware


class MiddlewareApp:
    def __init__(self):
        self.entity_storage_mid = EntityStorageMiddleware()
        self.tag_mid = TagMiddleware()


mid = MiddlewareApp()