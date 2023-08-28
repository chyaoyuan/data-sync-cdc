import asyncio

from channel.gllue.push.application.candidate.application import GlePushCandidate
from channel.gllue.push.application.client.application import GlePushClient
from channel.gllue.push.application.jobOrder.application import GlePushJobOrder


class GlePushApplication:
    def __init__(self, gle_user_config: dict):
        self.user_config = gle_user_config
        self.candidate_app = GlePushCandidate(self.user_config)
        self.client_app = GlePushClient(self.user_config)
        self.job_order_app = GlePushJobOrder(self.user_config)


if __name__ == '__main__':
    g = GlePushApplication({
        "apiServerHost": "https://www.cgladvisory.com",
        "aesKey": "398b5ec714c59be2",
        "account": "system@wearecgl.com"
    })
    #asyncio.run(g.client_app.put_client(info={"name":"mesoor-test5"}))
    # asyncio.run(g.client_app.put_job_order(info={"jobTitle": "测试项目1"}))
    asyncio.run(g.client_app.put_submission_candidate({}))
