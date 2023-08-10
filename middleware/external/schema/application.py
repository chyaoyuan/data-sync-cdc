import aiohttp
import urllib.parse as urlparse

from typing import Optional
from middleware.config import Settings
from middleware.exception import MiddlewareException
from middleware.external.base.application import Application as BaseApplication


class Application(BaseApplication):
    @staticmethod
    async def _get_internal_schema_info_response_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            response = await res.text()
            raise MiddlewareException("获取internal schema失败, url: {}, status: {}, response: {}".format(
                res.url.human_repr(), res.status, response
            ))
        result = await res.json()
        return result["link"]

    async def _get_internal_schema_info(self, tenant: str, name: str):
        result = await self.settings.session.get(
            self.settings.newest_schema_url.format(tenant=tenant, entityType=name),
            func=self._get_internal_schema_info_response_callback,
            ssl=False, timeout=120
        )
        result = urlparse.urlparse(result).path
        return result

    async def get_newest_schema_by_unique_name(self, tenant: str, name: str) -> Optional[str]:
        result = await self._get_internal_schema_info(tenant, name)
        return "{}#/properties/data".format(result)


def get_app():
    return Application(Settings)
