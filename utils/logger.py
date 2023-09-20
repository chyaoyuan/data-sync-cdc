import os
import sys

from loguru import logger

log_level = str(os.getenv('LOG_LEVEL', 'INFO')).upper()
# _defaults.LOGURU_FORMAT = default_format
logger.remove(handler_id=None)
# logger.add("file_2.log", rotation="12:00")

logger.add(sys.stdout, level=log_level)
logger.add(sys.stderr, level="WARNING")
