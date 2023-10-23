from typing import Literal, Optional, List, Union
from urllib.parse import quote,unquote
import urllib.parse
from middleware.settings.entitySorageSettings import parse_time_interval
from pydantic import BaseModel, Field, root_validator
from urllib.parse import parse_qs


# 同步规则
class ChildEntity(BaseModel):
    gql: Optional[str] = Field(description="覆写谷露筛选条件"),
    entityName: str = Field(title="同步的实体类型", examples="jobOrder")
    convertId: Optional[str] = Field(default="Job:sssssss")


class BaseSyncConfig(BaseModel):
    orderBy: Optional[str] = Field(default="-id", description="排序方式，详见谷露")
    syncModel: Union[Literal['GqlFilter'],
                     Literal["TimeRange"],
                     Literal["Recent"],
                     Literal["IdList"],
                     Literal["IdRecent"],
                     Literal["StringType"],
                     None] = Field(default=None, description="同步模式：GQL全局覆盖，时间范围，最近N单位，实体ID")
    syncAttachment: Optional[bool] = Field(default=True, description="是否同步附件【只有候选人有附件】")


class SyncConfig(BaseModel):
    convertId: Optional[str] = Field(default="Job:standard:2023_04_10_02_43_42")
    gql: Optional[str] = Field(default=None, description="覆写谷露筛选条件")
    idList: Optional[List[str]] = Field(default=None)
    fieldList: Optional[List[str]] = Field(default=[], description="同步该实体需要的额外字段(不需要请求gllueSchema)")
    childFieldList: Optional[list] = Field(default=[], description="同步该实体需要的额外字段(需要请求gllueSchema)")
    childEntityList: List[ChildEntity] = Field(default=[], description="同步有关系的的子实体，如职位下的候选人")




