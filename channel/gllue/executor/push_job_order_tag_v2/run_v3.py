import asyncio
import time

from channel.gllue.executor.push_job_order_tag_v2.push_job_order_tag_v3 import push_job_order_tag_exec_v3
from channel.gllue.executor.push_job_order_tag.settings.settings import Settings
from utils.logger import logger

from channel.gllue.executor.model import GleUserConfig, SyncConfig, TipConfig
from channel.gllue.executor.push_job_order_tag.push_job_order_tag_v2 import push_job_order_tag_exec

import time
# 因为标签接口不是很稳定，弃用了V2的workflow任务流配置写法，改为一波流请求
if __name__ == '__main__':
    sync_config = Settings.SyncConfig
    gle_user_config = Settings.GleUserConfig

    extra_config = Settings.ExtraConfig
    flows = Settings.FileSettings.flow_config[Settings.TipConfig.tenant_alias]
    while True:
        asyncio.run(
            push_job_order_tag_exec_v3(
                GleUserConfig(**gle_user_config),
                SyncConfig(**sync_config),
                Settings.TipConfig
            ))
        logger.info("sleeping")
        time.sleep(extra_config.time_sleep)
