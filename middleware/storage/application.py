from typing import Type
from middleware.config import Settings
from middleware.storage.file.application import Application as FileApplication
from middleware.storage.flows.application import Application as FlowsApplication
from middleware.storage.entity.application import Application as EntityApplication
from middleware.storage.channel.application import Application as ChannelApplication
from middleware.storage.project.application import Application as ProjectApplication


class Application:
    def __init__(self, settings: Type[Settings]):
        self.flows_app = FlowsApplication(settings)
        self.channel_app = ChannelApplication(settings)
        self.project_app = ProjectApplication(settings)
        self.entity_app = EntityApplication(settings)
        self.file_app = FileApplication(settings)


tip_space_application = Application(Settings)
