import asyncio
from typing import Type
import aiohttp
from loguru import logger
from middleware.settings.settings import Settings
from utils.custom_aiohttp_session import HoMuraSession


class BaseApplication():

    def __init__(self, settings: Type[Settings]):
        self.session: HoMuraSession = HoMuraSession(
            aiohttp.ClientSession, retry_when=lambda x: not isinstance(x, asyncio.exceptions.TimeoutError)
        )
        self.entity_storage_server_host = settings.EntityStorageSettings.entity_storage_server_host

    @staticmethod
    async def request_response_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            return await res.text(), res.status
        return await res.json(), res.status

    @staticmethod
    async def status_check_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            return await res.text(), res.status
        return await res.json(), res.status









