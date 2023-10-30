from typing import Optional


class IDCache:
    # 当同步发票的时候，会同时同步每张发票的User，User就那一点，没必要重复刷
    # 实现一种缓存，当本次同步过某一子实体，就不再同步此实体，记录上限为count_limit，超过上限随机移除一个
    def __init__(self, count_limit: Optional[int] = 20000):
        self.set = set()
        self.max_count = []
        self.count_limit = count_limit

    def add_id_one(self, entity_id):
        if len(self.set) < self.count_limit:
            self.set.add(entity_id)
        elif len(self.set) >= self.count_limit:
            self.set.pop()

    def check_exist(self, entity_id):
        return entity_id in self.set

    def del_id_one(self, entity_id):
        self.set.remove(entity_id)
