from typing import Optional

from pydantic import BaseModel, Field, Extra


class TaskPayload(BaseModel):
    openId: str = Field(description="简历openId")
    entityType: str


class Assignee(BaseModel):
    openId: Optional[str]


class Current(BaseModel):
    assignee: Optional[Assignee]


class Project(BaseModel):
    openId: str
    entityType: str


class StandardFields(BaseModel):
    taskPayload: TaskPayload
    current: Optional[Current]
    project: Project


class NewTask(BaseModel):
    standardFields: Optional[StandardFields]


class EventMessage(BaseModel):
    # newBeanRelation: Optional[NewBeanRelation]
    newTask: Optional[NewTask]
    project: str = Field(description="projectId")
    tenantId: str = Field(description="租户")


class EventBody(BaseModel):
    eventMessage: EventMessage
    data: str



