from typing import Union, Tuple

from dateutil.parser import parse as date_parse
import time
import re

from loguru import logger
from src.main.currency_model.email_receiver_model import EmailTimeDefault


def time_transformer(trans_time: Union[str, None] = 'Mon, 28 Feb 2022 16:30:50 +0800 (CST)'):
    """
        标准 Mon, 28 Feb 2022 16:30:50 +0800 (CST)
        非标准1 Fri, 4 Mar 2022 10:44:12 +0800 (GMT+08:00)
    """
    # try:
    if not trans_time:
        return EmailTimeDefault.defaultTime.strftime("%Y-%m-%d %H:%M:%S")
    # 兼容非标准2-Sun, 24 Apr 2022 11:14:27 +0800X-QQ-mid: bizesmtp64t1650770065t9ah23yz
    if re.search("\+0800.*",trans_time):
        trans_time = get_re_result(re.search(".*\+0800",trans_time))
    # 兼容非标准1
    if re.search(r'GMT\+08:00', trans_time):
        trans_time = re.sub(r'GMT\+08:00', "CST", trans_time)
    timestamp: float = date_parse(trans_time).timestamp()
    time_array = time.localtime(timestamp)
    _time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return _time
    # except Exception as e:
    #     logger.exception(e)
    #     return EmailTimeDefault.defaultTime