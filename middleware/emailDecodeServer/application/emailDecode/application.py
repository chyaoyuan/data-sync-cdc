from middleware.emailDecodeServer.application.base.base import BaseApplication
from middleware.emailDecodeServer.application.emailDecode.model import EmailDecodeServerRequest


class EmailDecodeApplication(BaseApplication):

    async def decode_email(self, data: dict):
        body = EmailDecodeServerRequest(**data)
        self.session.post
