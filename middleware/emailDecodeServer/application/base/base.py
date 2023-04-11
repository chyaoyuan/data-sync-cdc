import asyncio

import aiohttp

from utils.custom_aiohttp_session import HoMuraSession


class BaseApplication:
    def __init__(self):
        self.session = HoMuraSession(
            aiohttp.ClientSession, retry_when=lambda x: not isinstance(x, asyncio.exceptions.TimeoutError)
        )