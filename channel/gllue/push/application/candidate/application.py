from loguru import logger

from channel.gllue.push.application.base.application import BaseApplication


class GlePushCandidate(BaseApplication):

    async def push_candidate(self, entity: dict):
        info, status = await self.async_session.post(
            url=f"{self.gle_user_config.apiServerHost}/rest/candidate/add",
            gle_config=self.gle_user_config.dict(),
            ssl=False,
            json=entity,
            func=self.request_response_callback)
        if info["status"]:
            logger.info(f"候选人写回成功 id->{entity['id']}")
            return info
        else:
            logger.info(f"写回失败 id->{entity['id']} {info}")
