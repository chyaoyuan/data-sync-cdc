import asyncio

from channel.gllue.pull.application.applicaiton import GlePullApplication
_gle_user_config = {
                "apiServerHost": "https://fsgtest.gllue.net",
                "aesKey": "824531e8cad2a287",
                "account": "api@fsg.com.cn"
            }
_sync_config = {
        "entity": "candidate",
        "recent": "3",
        "unit": "day",
        "fieldName": "lastUpdateDate__lastUpdateDate__day_range",
        "gql": None,
    }


async def gle_sync_executor():
    job_order_app = GlePullApplication(_gle_user_config, _sync_config).job_order_app
    task_list = await job_order_app.run()
    for task in asyncio.as_completed(task_list):
        job_list: list = await task
        for job in job_list:
            print(job)
if __name__ == '__main__':
    asyncio.run(gle_sync_executor())