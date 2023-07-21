import asyncio
from typing import Type

import requests
from loguru import logger

from channel.gllue.database.executor.executor_application import DataBaseExecutorApplication
from channel.gllue.pull.application.applicaiton import GlePullApplication
from channel.gllue.config import Settings
from middleware.mdwConvert.convert_middleware import ConvertMiddleware
convert_middleware = ConvertMiddleware()


class GleExecutor:
    headers = {
        'X-Source': 'gllue-new-job',
        'X-Editor': 'gllue-new-job',
        'Content-Type': 'application/json'
    }

    def __init__(self, user_config: dict, settings: Type[Settings]):
        self.user_config = user_config
        self.gle_pull_app = GlePullApplication(user_config)
        self.gle_db_app = DataBaseExecutorApplication(settings)
        self.gle_db_app.init_tables()

    async def get_gle_job_form_gle_to_database(self):
        """从谷露系统获取JOB存到数据库"""
        job_order_list = await self.gle_pull_app.job_order_app.run()
        logger.info(job_order_list)
        for job_order in job_order_list:
            logger.info(job_order)
            id = f"Gllue-Job-{self.user_config['tenant']}-{job_order['id']}"
            logger.info({"id": id, "sourceId": job_order["id"], "payload": job_order, "tenant": self.user_config["tenant"],"entityType":"Job"})
            await self.gle_db_app.entity.put_entity(
                {"sourceId": job_order["id"], "id": f"Gllue-Job-{self.user_config['tenant']}-{job_order['id']}", "payload": job_order, "tenant": self.user_config["tenant"],"entityType":"Job"}
            )

    async def get_gle_job_form_database(self):
        """从谷露系统获取JOB存到数据库"""

        ids = await self.gle_db_app.entity.get_all_ids_by_tenant(self.user_config["tenant"], "Job")
        for _id in ids:
            entity_info = await self.gle_db_app.entity.get_entity_by_unique_id(unique_id=_id)
            logger.info(entity_info)
            standard_fields = await convert_middleware.convert.convert(
                {"task_ids": ["Job:standard:2023_04_10_02_43_42"], "data": [{"sourceData": entity_info["payload"]}]})
            body = {
                "rawData": {
                    "content": {"sourceData": entity_info["payload"]}
                },
                "standardFields": standard_fields}
            url = f"http://ruleengine.nadileaf.com/v2/entity/5jlh62781a6zw/Job/{entity_info['id']}"
            response = requests.request("PUT", url, headers=self.headers, json=body)
            if response.status_code == 200:
                logger.info(f"成功 openid->{entity_info['id']}")
            else:
                logger.error(response.text)




if __name__ == '__main__':
    asyncio.run(GleExecutor(
        {
            "apiServerHost": "https://fsgtest.gllue.net",
            "aesKey": "824531e8cad2a287",
            "account": "api@fsg.com.cn",
            "tenant": "5jlh62781a6zw"
        }
    ,Settings).get_gle_job_form_database())
