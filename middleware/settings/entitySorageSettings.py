import os
from datetime import datetime, timedelta
import pytz


class EntityStorageSettings:
    entity_storage_server_host = os.getenv("Entity_Storage_Server_HOST","http://localhost:9400")


def parse_time_interval(time_interval: dict):
    unit = time_interval["unit"]
    recent = int(time_interval["recent"])-1

    # 获取当前时间（中国时区）
    tz = pytz.timezone('Asia/Shanghai')
    current_time = datetime.now(tz)

    # 根据单位调整起始时间
    if unit == "year":
        start_time = current_time - timedelta(days=recent * 365)
    elif unit == "month":
        start_time = current_time - timedelta(days=recent * 30)
    elif unit == "day":
        start_time = current_time - timedelta(days=recent)
    else:
        raise ValueError("Invalid unit value!")

    # 格式化时间
    start_time_str = start_time.strftime("%Y-%m-%d")
    current_time_str = current_time.strftime("%Y-%m-%d")
    return start_time_str, current_time_str

if __name__ == '__main__':
    parse_time_interval({
        "entity": "candidate",
        "recent": "1",
        "unit": "year",
        "gql": None,
    })
