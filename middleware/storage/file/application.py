import aiohttp

from typing import Union
from typing_extensions import Literal
from utils.logger import logger
from middleware.exception import MiddlewareException
from middleware.storage.file.model import SaveFileBody, SaveB64FileBody
from middleware.storage.base.application import Application as BaseApplication


class Application(BaseApplication):
    @staticmethod
    async def save_file_response(res: aiohttp.ClientResponse):
        result = await res.json()
        return res.status, result

    async def _save_file(self, body: Union[SaveB64FileBody, SaveFileBody], mode: Literal['b64', 'file']):
        if mode == "file":
            form_data = aiohttp.FormData()
            form_data.add_field("file", body.fileContent, filename=body.fileName)
            params = {"key": body.key} if body.key else None
            status, response = await self.settings.session.put(
                self.settings.save_file_url, data=form_data, ssl=False, timeout=300, func=self.save_file_response,
                params=params
            )
        else:
            params = {"key": body.key} if body.key else None
            status, response = await self.settings.session.put(
                self.settings.save_b64_file_url, json={
                    "content": body.fileContent, "fileName": body.fileName
                }, ssl=False, timeout=300, func=self.save_file_response, params=params
            )
        if status != 200:
            raise MiddlewareException("存储文件 {} 失败, 原因: {}".format(
                body.fileName, response.get("message") or "未知原因"
            ))
        logger.info("存储文件 {} 成功".format(
            response["result"]["key"]
        ))
        return response["result"]["key"]

    async def save_file(self, body: dict) -> str:
        body = SaveFileBody(**body)
        return await self._save_file(body, "file")

    async def save_b64_file(self, body: dict) -> str:
        body = SaveB64FileBody(**body)
        return await self._save_file(body, "b64")
