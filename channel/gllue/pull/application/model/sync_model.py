from typing import Literal, Optional, List
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


class SyncConfig(BaseModel):
    syncAttachment: Optional[bool] = Field(default=False, description="是否同步附件【只有候选人有附件】")
    convertId: Optional[str] = Field(default="Job:standard:2023_04_10_02_43_42")
    gql: Optional[str] = Field(default=None, description="覆写谷露筛选条件")
    recent: Optional[int] = Field(default=None, title="同步数", examples=3)
    unit: Optional[Literal['year', 'month', 'day']] = Field(default=None, description="recent的单位")
    # 添加日期、MPC添加日期,最后更新时间、最近操作、最近联系
    timeFieldName: Optional[
        Literal[
            'dateAdded__day_range',
            'mpcDate__day_range',
            'lastUpdateDate__day_range',
            'latest_action__day_range',
            'lastContactDate__day_range']] = Field(default=None, description="时间段筛选的字段，如添加日期、最后更新时间")
    fieldList: Optional[list] = Field(default=[], description="同步该实体需要的额外字段(不需要请求gllueSchema)")
    childFieldList: Optional[list] = Field(default=[], description="同步该实体需要的额外字段(需要请求gllueSchema)")
    childEntityList: List[ChildEntity] = Field(default=[], description="同步有关系的的子实体，如职位下的候选人")

    @root_validator(pre=True)
    def generate_and_validate_additional_field(cls, values):
        # 如果客户填写了谷露的GQL我这边就不会去生成/补全任何ZZZ
        if gql := values["gql"]:
            return values
        # 将时间参数生成进GQL里
        if (unit := values["unit"]) and (recent := values["recent"]):
            start_time, end_time = parse_time_interval({"unit": unit, "recent": recent})
            gql = values["timeFieldName"] + "=" + quote(start_time + "," + end_time)
            values["gql"] = gql
        return values



