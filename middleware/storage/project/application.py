import aiohttp

from utils.logger import logger
from middleware.exception import MiddlewareException
from middleware.storage.project.model import ProjectBody, ProjectFlowStageBody
from middleware.storage.base.application import Application as BaseApplication


class Application(BaseApplication):
    @staticmethod
    async def save_project_response_callback(res: aiohttp.ClientResponse):
        result: dict = await res.json()
        return result, res.status

    async def save_project(self, body: dict, auth: str):
        request_body = ProjectBody(**body)
        response, status = await self.settings.session.put(
            self.settings.save_project_url,
            headers={
                "Authorization": auth
            },
            json=request_body.dict(),
            func=self.save_project_response_callback,
            ssl=False, timeout=120
        )
        result = response["result"]
        if status != 200:
            raise MiddlewareException("存储project出错, project id: {}, channel id: {} status code: {} 原因: {}".format(
                request_body.projectId, request_body.channelId, status, response.get("message") or "未知原因"
            ))
        logger.info("{} project 成功 project id: {} job id: {}".format(
            "更新" if result.get("status") == "U" else "存储",
            result.get("projectId") or "未知",
            result.get("jobId") or "未知"
        ))

    @staticmethod
    async def save_project_flow_stage_response_callback(res: aiohttp.ClientResponse):
        result = await res.json()
        return result, res.status

    async def save_project_flow_stage(self, body: dict, auth: str):
        request_body = ProjectFlowStageBody(**body)
        response, status = await self.settings.session.put(
            self.settings.save_project_stage_url,
            json=request_body.dict(), func=self.save_project_flow_stage_response_callback,
            ssl=False, timeout=120, headers={"Authorization": auth}
        )
        if status != 200:
            raise MiddlewareException("更新 project flow stage 失败, status: {}, 原因: {}".format(
                status, response.get("message") or "未知原因"
            ))
        if response["result"]["flowStageNames"]:
            logger.info("更新 project flow stage 成功, stage names: {}".format(response["result"]["flowStageNames"]))
