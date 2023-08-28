from typing import Literal

from pydantic import BaseModel


class EntityChangeInfo(BaseModel):
    status: Literal["create", "update"]
    entityType: Literal["candidate", "jobSubMission", "jobOrder", "client"]
    id: str


class EntityChangeLog:
    def __init__(self):
        self.log = []

    def add_log(self, status: str, entity_type: str, _id: str):
        self.log.append(EntityChangeInfo(**{"status": status, "entityType": entity_type, "id": _id}))

    def get_log(self):
        return [log.dict() for log in self.log]