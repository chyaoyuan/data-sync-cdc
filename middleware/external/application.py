from typing import Type
from middleware.config import Settings
from middleware.external.schema.application import get_app as get_schema_app
from middleware.external.convert.application import get_app as get_convert_app
from middleware.external.base.application import Application as BaseApplication
from middleware.external.cvparser.application import get_app as get_resume_parser_app
from middleware.external.transmitter.application import get_app as get_transmitter_app


class Application(BaseApplication):
    def __init__(self, settings: Type[Settings]):
        super().__init__(settings)
        self.transmitter_app = get_transmitter_app()
        self.convert_app = get_convert_app()
        self.schema_app = get_schema_app()
        self.resume_parser = get_resume_parser_app()


def get_app():
    return Application(Settings)


external_application = Application(Settings)
