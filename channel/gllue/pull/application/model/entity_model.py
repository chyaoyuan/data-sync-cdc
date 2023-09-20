from typing import Optional

from pydantic import BaseModel


class GleEntity:
    def __init__(self, data: dict):
        self.data = data
        self.entityType = self.__class__.__name__
        setattr(self, f"{self.entityType}Id", data["id"])


class Client(GleEntity):
    def __init__(self, data: dict):
        super().__init__(data)
        self.entityType = self.__class__.__name__
        setattr(self, f"{self.entityType}Id", data["id"])
        self.job_order: Optional[JobOrder] = None


class JobOrder(GleEntity):
    def __init__(self, data: dict):
        super().__init__(data)
        self.entityType = self.__class__.__name__
        setattr(self, f"{self.entityType}Id", data["id"])


class Candidate(JobOrder):
    def __init__(self, data: dict):
        super().__init__(data)
        self.entityType = self.__class__.__name__
        setattr(self, f"{self.entityType}Id", data["id"])


class JobSubMission(Candidate):
    def __init__(self, data: dict):
        super().__init__(data)
        self.entityType = self.__class__.__name__
        setattr(self, f"{self.entityType}Id", data["id"])

