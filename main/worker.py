import asyncio
import json
import os
from typing import List
from urllib.parse import quote_plus as urlquote
from celery import Celery
from utils.logger import logger

from channel.gllue.executor.application import GleExeApp
from channel.gllue.executor.pull_candidate.sync import pull_candidate as pull_gle_candidate
from main.settings import Settings

app = Celery(
    'worker', broker=Settings.redis_broker,
    backend=f'db+postgresql://{Settings.pg_user}:{urlquote(Settings.pg_password)}@{Settings.pg_host}:{Settings.pg_port}/{Settings.pg_database}'
)

# 同步谷露人才数据
@app.task(name="SyncGllueCandidate")
def receive_gle_candidate(config: str):
    params = json.loads(config)
    tip_config = params["tipConfig"]
    gle_config = params["gllueConfig"]
    sync_config = params["syncConfig"]
    sync_config_list: List[dict] = GleExeApp(sync_config, gle_config, tip_config).map_sync_config()
    loop = asyncio.get_event_loop()
    for index, _sync_config in enumerate(sync_config_list):
        loop.run_until_complete(pull_gle_candidate(gle_config, _sync_config, tip_config))


