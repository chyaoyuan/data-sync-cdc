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


_gle_user_config = {
        "apiServerHost": "https://www.cgladvisory.com",
        "aesKey": "398b5ec714c59be2",
        "account": "system@wearecgl.com",
    }
base_sync_config = {
    "syncModel": "Id",
    "syncAttachment": False,
}
_sync_config = {

    "storageModel": "Local",
    "jsonFileStorageName": "res_20231007.jsonl",
    "FileStoragePath": "res_20231007.jsonl",
    "startTime": "2023-08-01 00:00:00",
    "endTime": "2023-09-01 00:00:00",
    "recent": "1",
    "unit": "month",
    "timeFieldName": "dateAdded__day_range",
    "idList": [],
    "convertId": "Resume:standard:2023_09_04_03_27_59",
    "fieldList": ["attachments", "tags", "functions", "industrys", "locations",],
    "childFieldList": ["candidateeducation", "candidateexperience", "candidateproject", "candidatelanguage", "candidatequalification"],
}

# 确定基础同步信息，参数预处理
class SyncConfig(BaseModel):
    primaryEntityName: str
    tipEntityName: str
    syncAttachment: Optional[bool] = Field(default=False, description="同步以附件解析为主【只有候选人有附件】")
    syncModel: Union[Literal['GqlFilter'],
                     Literal["TimeRange"],
                     Literal["Recent"],
                     Literal["IdList"],
                     Literal["IdRecent"],
                     Literal["StringType"],
                     None] = Field(default=None, description="同步模式：GQL全局覆盖，时间范围，最近N单位，实体ID")
    storageModel: Union[Literal['Tip'], Literal['Local'], None] = Field(default=None, description="存入Tip、写本地文件")
    jsonFileStorageName: Optional[str] = Field(default=None, description="写本地文件名称")
    storagePath: Optional[str] = Field(default=None, description="写本地文件模式文件路径，jsonl追加写,file存文件对象")

    jsonFileStoragePath: Optional[str] = Field(default=None, description="json-写本地文件路径")
    baseAttachmentFileStoragePath: Optional[str] = Field(default=None, description="附件-写本地文件路径")

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
        Literal['lastContactDate__day_range'], None] = Field(default="lastUpdateDate__day_range", description="时间段筛选的字段，如添加日期、最后更新时间")
    # ID
    idList: Optional[List[int]] = Field(default=[], description="实体ID列表")
    # IdRecent
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
        assert sync_model
        # 除了ID同步模式【IdList、IdRecent】，其他都使用gql参数作为筛选条件
        if values.get("gql") and sync_model == "GqlFilter":
            pass
        elif sync_model == "IdList":
            assert values["idList"]

        elif sync_model == "IdRecent":
            id_recent = values["IdRecent"]
            min_index = int(id_recent.split("-")[0])
            max_index = int(id_recent.split("-")[1])
            values["idList"] = [i for i in range(min_index, max_index+1)]
        elif sync_model == "TimeRange":
            gql = values["timeFieldName"] + "=" + quote(start_time + "," + end_time)
            values["gql"] = gql
        # 将时间参数生成进GQL里

        elif sync_model == "Recent" and unit and recent:
            start_time, end_time = parse_time_interval({"unit": unit, "recent": recent})
            gql = values["timeFieldName"] + "=" + quote(start_time + "," + end_time)
            values["gql"] = gql
        if values["storageModel"] == "Local":
            path = values["storagePath"]
            values["jsonFileStoragePath"] = f'{path}/{values["primaryEntityName"]}'
            values["baseAttachmentFileStoragePath"] = f'{path}/{values["primaryEntityName"]}'

        return values
# Tip配置


class TipConfig(BaseModel):
    Authorization: Optional[str]
    # spaceId: str
    userId: Optional[str]
    tenantAlias: str

    @classmethod
    def transform(cls, source_data: dict):
        if not source_data.get("jwtToken"):
            return cls(
            **source_data
        )

        token_not_bearer = source_data["jwtToken"].replace("Bearer ", "")
        user_info = jwt.decode(token_not_bearer, algorithms=["HS512"], options={"verify_signature": False})
        return cls(
            Authorization=source_data["jwtToken"],
            tenantAlias=user_info["tenantAlias"],
            userId=user_info["userId"],
            spaceId=source_data["spaceId"]
        )


