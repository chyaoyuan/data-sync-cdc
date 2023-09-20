import asyncio
import time

from utils.logger import logger

from channel.gllue.executor.model import GleUserConfig, SyncConfig, TipConfig
from channel.gllue.executor.push_job_order_tag.push_job_order_tag import push_job_order_tag_exec

import time

if __name__ == '__main__':
    _gle_user_config = {
        "apiServerHost": "https://fsgtest.gllue.net",
        "aesKey": "824531e8cad2a287",
        "account": "api@fsg.com.cn"
    }
    _sync_config = {
        "entityName": "jobOrder",
        "recent": "3",
        "unit": "day",
        "timeFieldName": "lastUpdateDate__day_range",
    }

    _tip_config = {
        "jwtToken": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VybmFtZTo4NjE3NjEyMzA1NzE2IiwidGVuYW50SWQiOjEwMDAxNDksImlzcyI6ImRlZmF1bHQiLCJ0ZW5hbnRBbGlhcyI6Im5iMWwxMDAwMTQ5cXo1NXgiLCJleHAiOjE2OTI4NjMyNzg0MjksInVzZXJJZCI6IjJhOGZmNjE2LTZlMTQtNDQ2MS04YjRkLTJhM2ZkZDAxOTMzNyIsInByb2plY3RJZCI6ImRlZmF1bHQiLCJpYXQiOjE2OTE2NTM2Nzg0Mjl9.d9F4MKQq_kv7AKbTq3YdrSTZrhTqPmQhEQTS7mrb0nw",
        "spaceId": "5ea8b9c6-373f-4641-8f3f-07cc46128ed9",
    }
    while True:
        asyncio.run(
            push_job_order_tag_exec(
                GleUserConfig(**_gle_user_config),
                SyncConfig(**_sync_config),

            ))
        logger.info("dengdai")
        print(999999999)
        time.sleep(180)
