import json
from loguru import logger


class App:
    @staticmethod
    def get_tip_exist_openid():
        with open("/Volumes/Expansion/CGL202310/tip_exist_20231008.json") as f:
            ids = json.loads(f.read())
        ids = [int(_id.get("openid").replace("gllue-", "")) for _id in ids]
        max_id = max(ids)
        min_id = min(ids)
        logger.info(f"sun->{len(ids)}")
        logger.info(f"max->{max_id}")
        logger.info(f"min->{min_id}")


if __name__ == '__main__':
    App().get_tip_exist_openid()