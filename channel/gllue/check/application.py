import json
from loguru import logger


class App:
    def base_file_io(self,path: str):
        with open(path) as f:
            ids = json.loads(f.read())
        ids = [int(_id.get("openid").replace("gllue-", "")) for _id in ids]
        max_id = max(ids)
        min_id = min(ids)
        logger.info(f"sun->{len(ids)}")
        logger.info(f"max->{max_id}")
        logger.info(f"min->{min_id}")
        return set([i for i in range(1,max_id+1)])- set(ids)
    def get_tip_exist_openid(self):
        ids = self.base_file_io("/Volumes/Expansion/CGL202310/tip_exist_20231008.json")
        return ids

    def get_gle_not_exist(self):
        with open("/Volumes/Expansion/CGL202310/gllue_not_exist_id_20230928.json") as f:
            ids = set(json.loads(f.read()))
            return ids

    def guess(self):
        ids = self.get_tip_exist_openid()-set(self.get_gle_not_exist())
        print(len(ids))
        with open("/Volumes/Expansion/CGL202310/gllue_maybe_exist_id_20231012.json","w") as f:
            f.write(json.dumps(list(ids), ensure_ascii=False))


if __name__ == '__main__':
    App().guess()