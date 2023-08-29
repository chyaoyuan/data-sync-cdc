from typing import Literal, List, Optional
import jwt
from pydantic import BaseModel, Field


# 谷露配置
class GleUserConfig(BaseModel):
    apiServerHost: str = Field(title="客户谷露系统的Host", description="https://www.cgladvisory.com",)
    aesKey: str = Field(title="客户在谷露系统申请的aesKey", description="ae48bf2137cd656",)
    account: str = Field(title="客户在谷露系统的账户名,一般为注册邮箱", description="sysewm@qq.com")


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


