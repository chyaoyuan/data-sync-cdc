import aiohttp

from loguru import logger
from middleware.exception import MiddlewareException
from middleware.storage.flows.model import FlowsBody
from middleware.storage.base.application import Application as BaseApplication


class Application(BaseApplication):
    @staticmethod
    async def add_flow_response_callback(res: aiohttp.ClientResponse):
        result: dict = await res.json()
        return result, res.status

    async def add_flow(self, body: dict, auth: str):
        request_body = FlowsBody(**body)
        response, status = await self.settings.session.post(
            self.settings.move_flow_url,
            headers={
                "Authorization": auth
            },
            func=self.add_flow_response_callback,
            json=request_body.dict(),
            ssl=False, timeout=120
        )
        result = response["result"]
        if status != 200:
            raise MiddlewareException("{} 添加 {} 进入流程 {} 出错, status code: {} 原因: {}".format(
                request_body.projectId, request_body.entityId, request_body.stageName, status,
                response.get("message") or "未知原因"
            ))
        logger.info("创建 {}, 更新 {} 至 project {} 流程 {} 成功".format(
            result["createEntityIds"], result["updateEntityIds"], result["projectId"], result["stage"]
        ))
