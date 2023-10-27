import json
import re
import urllib.parse
from urllib.parse import urlencode
import aiohttp
import asyncio
from utils.logger import logger
from aiohttp.typedefs import StrOrURL
from typing import Type, Callable, Optional, Any, Coroutine
import time
__all__ = ("GlHoMuraSession", )

from channel.gllue.session.create_token import private_token


def login_in_gle_form_data(gle_user_config):
    fd = aiohttp.FormData()
    sttt = json.dumps({
        "password": gle_user_config['extraPassword'],
        "remember": True,
        "next": "/",
        "email": gle_user_config['extraAccount'],
        "lang": "zh_CN"}, ensure_ascii=False)
    fd.add_field("data", sttt)
    return fd


class GlHoMuraSession:
    def __init__(
            self, client_session: Type[aiohttp.ClientSession], gle_user_config: dict, *, retry_time: int = 5,
            retry_interval: Optional[int] = 60, retry_when: Optional[Callable] = None,
            exception_class: Optional[Any] = None, exception_kwargs: Optional[dict] = None
    ):
        self.client_session = client_session
        self.retry_time = retry_time
        self.retry_interval = retry_interval
        self.retry_when = retry_when
        self.exception_class = exception_class
        self.exception_kwargs = exception_kwargs
        self.gle_user_config = gle_user_config

    async def request(
        self, method: str, url: StrOrURL, func: Callable, ssl=False, **kwargs
    ):
        async with self.client_session() as session:
            not_use_token = kwargs.pop("not_use_token", None)
            if not not_use_token:
                params = kwargs["params"] if "params" in kwargs.keys() else {}
                token = private_token(self.gle_user_config)
                # logger.info(f"gllue_private_token->{urllib.parse.quote(token)}")
                params["gllue_private_token"] = token
                params = {k: v for k, v in params.items() if v}
                kwargs["params"] = params
            url = f"{self.gle_user_config['apiServerHost']}{url}"
            last_error = Exception("")
            for i in range(self.retry_time):
                try:
                    res = await session.request(method.upper(), url, ssl=ssl, **kwargs)
                    # if res.status == 200:
                    #     info = await res.json()
                    #     if isinstance(info, dict) and "所访问的url不在允许范围之内" in info.get("message",""):
                    #         kwargs.get("params",{}).pop("gllue_private_token", None)
                    #         logger.warning(f"aeskey缺少权限->{url}->{info}")
                    #         login_in_url = f"{self.gle_user_config['apiServerHost']}/rest/user/login"
                    #         logger.info(login_in_url)
                    #         login_in_res = await session.post(login_in_url, data=login_in_gle_form_data(self.gle_user_config),
                    #                                     ssl=ssl, **kwargs)
                    #         if not info.get("status"):
                    #             logger.error(f"登陆失败->{info}")
                    #         uid_cookie = login_in_res.cookies.get("uid").value
                    #
                    #         kwargs["headers"] = {"cookies": f"uid={uid_cookie}"}
                    #         res = await session.request(method.upper(), url, ssl=ssl, **kwargs)
                    break
                except Exception as _e:
                    if self.exception_class is None or self.exception_class is Exception:
                        last_error = _e
                    else:
                        last_error = self.exception_class(
                            "error message: {}".format(repr(_e)), **self.exception_kwargs or {}
                        )
                    if self.retry_when and not self.retry_when(_e):
                        raise last_error
                    logger.error("retry to request url: {}, method: {}, now request time: {}".format(
                        url, method, i + 1
                    ))
                    if self.retry_interval is not None:
                        await asyncio.sleep(self.retry_interval)
                    continue
            else:
                raise last_error
            call_result = func(res)
            if isinstance(call_result, Coroutine):
                result = await call_result
            else:
                result = call_result

        return result

    async def get(self, url: StrOrURL, *, func: Callable, allow_redirects: bool = True, **kwargs):

        return await self.request('get', url, func=func, allow_redirects=allow_redirects, **kwargs)

    async def post(self, url: StrOrURL, *, func: Callable, data: Any = None, **kwargs):
        return await self.request('post', url, func=func, data=data, **kwargs)

    async def put(self, url: StrOrURL, *, func: Callable, data: Any = None, **kwargs):
        return await self.request('put', url, func=func, data=data, **kwargs)

    async def patch(self, url: StrOrURL, *, func: Callable, **kwargs):
        return await self.request('patch', url, func=func, **kwargs)

    async def delete(self, url: StrOrURL, *, func: Callable, **kwargs):
        return await self.request('delete', url, func=func, **kwargs)


async def callback(res: aiohttp.ClientResponse) -> tuple:
    if res.status == 200:
        return res.status, await res.json()
    return res.status, await res.text()


# async def main():
#     class D:
#         def __init__(self, c: str):
#             self.c = c
#
#         async def callback(self, res: aiohttp.ClientResponse):
#             print(self.c)
#             return await res.text()
#
#     url = "http://localhost:8088/test"
#     session = HoMuraSession(
#         aiohttp.ClientSession, retry_when=lambda x: not isinstance(x, asyncio.exceptions.TimeoutError)
#     )
#     r = await session.get(url, func=D("10").callback, headers={
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) "
#                       "Chrome/99.0.4844.51 Safari/537.36"
#     }, ssl=False, timeout=60)
#     print(r)
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
