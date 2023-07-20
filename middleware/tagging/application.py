from middleware.tagging.tag.application import TagApplication
from middleware.settings.settings import Settings


class TagMiddleware:
    def __init__(self):
        self.tag_app = TagApplication(Settings)