from typing import Literal, List, Optional

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


class SyncConfig(BaseModel):
    entityName: str = Field(title="同步的实体类型", examples="jobOrder")
    fieldName: List['str'] = Field(default=[], description="实体同步的额外字段")
    gql: Optional[str] = Field(description="覆写谷露筛选条件")
    recent: int = Field(title="同步数", examples=3)
    unit: Literal['year', 'month', 'day'] = Field(description="recent的单位")
    childEntityList: List[ChildEntity] = Field(default=[], description="同步有关系的的子实体，如职位下的候选人")

# Tip配置


class TipConfig(BaseModel):
    Authorization: str
    spaceId: str
    userId: str
    tenantAlias: str
tip_config = {
    "jwtToken": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VybmFtZTo4NjE3NjEyMzA1NzE2IiwidGVuYW50SWQiOjYyODIsImlzcyI6ImRlZmF1bHQiLCJ0ZW5hbnRBbGlhcyI6ImFnOTM2Mjgya3pxZW0iLCJleHAiOjE2OTI3ODA2NjIwMjIsInVzZXJJZCI6IjJhOGZmNjE2LTZlMTQtNDQ2MS04YjRkLTJhM2ZkZDAxOTMzNyIsInByb2plY3RJZCI6ImRlZmF1bHQiLCJpYXQiOjE2OTE1NzEwNjIwMjJ9.KXY0ZsuTCYBiGv4vaz1gEwlJEMHo_E8Y8WDP7Sf2gTo",
    "spaceId": "fb6b3b31-2c2c-4e5f-9363-d51c6720d999",
    "tenantId": ""

}
