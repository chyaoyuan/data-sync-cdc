from typing import Literal, List, Optional, Union
import jwt
from pydantic import BaseModel, Field, root_validator
from typing import Literal, Optional, List
from urllib.parse import quote,unquote
import urllib.parse
from middleware.settings.entitySorageSettings import parse_time_interval
from pydantic import BaseModel, Field, root_validator
from urllib.parse import parse_qs


# 谷露配置
class GleUserConfig(BaseModel):
    apiServerHost: str = Field(title="客户谷露系统的Host", description="https://www.cgladvisory.com",)
    aesKey: str = Field(title="客户在谷露系统申请的aesKey", description="ae48bf2137cd656",)
    account: str = Field(title="客户在谷露系统的账户名,一般为注册邮箱", description="sysewm@qq.com")


# 同步规则
class ChildEntity(BaseModel):
    entityName: str = Field(title="同步的实体类型", examples="jobOrder")
    convertId: Optional[str] = Field(default="Job:sssssss")


class SyncConfig(BaseModel):
    entityName: str
    syncAttachment: Optional[bool] = Field(default=False, description="同步以附件解析为主【只有候选人有附件】")
    syncModel: Union[Literal['GqlFilter'], Literal[ "TimeRange"], Literal["Recent"], Literal["Id"], None] = Field(default=None,description="同步模式：GQL全局覆盖，时间范围，最近N单位，实体ID")
    storageModel: Union[Literal['Tip'], Literal['Local'], None] = Field(default=None, description="存入Tip、写本地文件")
    fileStoragePath: Optional[str] = Field(default=None, description="写本地文件模式文件路径及名称，追加写，examples=result.jsonl")
    orderBy: Optional[str] = Field(default="-id", description="同步数据排序方式")
    # GQL 同步模式
    gql: Optional[str] = Field(default=None, description="覆写谷露筛选条件")
    # 最近N单位
    recent: Optional[int] = Field(default=None, title="同步数", examples=3)
    unit: Optional[Literal['year', 'month', 'day']] = Field(default=None, description="recent的单位")
    # 时间段
    startTime: Optional[str] = Field(default=None)
    endTime: Optional[str] = Field(default=None)
    # 添加日期、MPC添加日期,最后更新时间、最近操作、最近联系
    timeFieldName: Union[
        Literal['dateAdded__day_range'],
        Literal['mpcDate__day_range'],
        Literal['lastUpdateDate__day_range'],
        Literal['latest_action__day_range'],
        Literal['lastContactDate__day_range'], None] = Field(default=None, description="时间段筛选的字段，如添加日期、最后更新时间")
    # ID
    idList: Optional[List[str]] = Field(default=[], description="实体ID列表")
    fieldList: Optional[list] = Field(default=[], description="同步该实体需要的额外字段(不需要请求gllueSchema)")
    childFieldList: Optional[list] = Field(default=[], description="同步该实体需要的额外字段(需要请求gllueSchema)")
    extraEntity: List[ChildEntity] = Field(default=[], description="同步有关系的的子实体，如职位下的候选人")
    convertId: Optional[str] = Field(default="Job:standard:2023_04_10_02_43_42")

    @root_validator(pre=True)
    def generate_and_validate_additional_field(cls, values):
        # 如果客户填写了谷露的GQL我这边就不会去生成/补全任何ZZZ
        sync_model = values["syncModel"]
        start_time = values.get("startTime")
        end_time = values.get("endTime")
        unit = values.get("unit")
        recent = values.get("recent")
        if not sync_model:
            return values
        if values.get("gql") and sync_model == "GqlFilter":
            return values

        elif sync_model == "TimeRange":
            gql = values["timeFieldName"] + "=" + quote(start_time + "," + end_time)
            values["gql"] = gql
        # 将时间参数生成进GQL里

        elif sync_model == "Recent" and unit and recent:
            start_time, end_time = parse_time_interval({"unit": unit, "recent": recent})
            gql = values["timeFieldName"] + "=" + quote(start_time + "," + end_time)
            values["gql"] = gql
        return values
# Tip配置


class TipConfig(BaseModel):
    Authorization: str
    spaceId: str
    userId: str
    tenantAlias: str

    @classmethod
    def transform(cls, source_data: dict):
        token_not_bearer = source_data["jwtToken"].replace("Bearer ", "")
        user_info = jwt.decode(token_not_bearer, algorithms=["HS512"], options={"verify_signature": False})
        return cls(
            Authorization=source_data["jwtToken"],
            tenantAlias=user_info["tenantAlias"],
            userId=user_info["userId"],
            spaceId=source_data["spaceId"]
        )


