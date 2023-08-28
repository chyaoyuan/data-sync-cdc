from typing import Literal, Optional, List

from pydantic import BaseModel, Field


# 同步规则
class ChildEntity(BaseModel):
    gql: Optional[str] = Field(description="覆写谷露筛选条件"),
    entityName: str = Field(title="同步的实体类型", examples="jobOrder")
    convertId: Optional[str] = Field(default="Job:sssssss")


class SyncConfig(BaseModel):
    entityName: str = Field(title="同步的实体类型", examples="jobOrder")
    fieldNameList: Optional[str] = Field(default=None, description="实体同步的额外字段")
    convertId: Optional[str] = Field(default="Job:standard:2023_04_10_02_43_42")
    gql: Optional[str] = Field(description="覆写谷露筛选条件")
    recent: int = Field(title="同步数", examples=3)
    unit: Literal['year', 'month', 'day'] = Field(description="recent的单位")
    timeFieldName: Literal['lastContactDate__lastContactDate__day_range', 'lastUpdateDate__lastUpdateDate__day_range'] = Field(description="时间段筛选的字段，如最后联系时间、最后更新时间")
    childEntityList: List[ChildEntity] = Field(default=[], description="同步有关系的的子实体，如职位下的候选人")