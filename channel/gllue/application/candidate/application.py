import asyncio
import base64
from cgi import parse_header
from typing import Optional, Literal, List
from urllib.parse import unquote
from loguru import logger
from pydantic import BaseModel, Field

from channel.gllue.application.schema.application import GleSchema
from channel.gllue.application.base.model import BaseResponseModel


class SyncConfig(BaseModel):
    entity: str
    recent: int = Field(..., description="近 n 天/月/年", example=10)
    unit: Literal['day', 'month', 'year'] = Field(default="day", description="单位", example="day")
    gql: Optional[str] = Field(default=None, description="可以指定gllueGQL")


class GleEntity(GleSchema):
    # 每页最大条数
    total_count: int = 10

    def __init__(self, gle_user_config: dict, sync_config: dict):
        super().__init__(gle_user_config)
        self.sync_config = SyncConfig(**sync_config)

        self.entity = self.sync_config.entity
        # if self.sync_config.unit and self.sync_config.recent:

        self.add_child_field_list = ["candidateexperience","candidatequalification","candidatelanguage","candidateproject"]

    async def _get_candidate_info(self, page: int, field_name_list: str, check: bool):
        res, status = await self.async_session.get(
            url=f"{self.gle_user_config.apiServerHost}/rest/{self.entity}/simple_list_with_ids",
            gle_config=self.gle_user_config.dict(),
            ssl=False,
            params={"fields": field_name_list,
                    "ordering": "-lastUpdateDate",
                    "paginate_by": self.total_count,
                    'page': page,
                    # 'gql': "lastUpdateDate__today"

                    },
            func=self.request_response_callback)
        if check:
            return res
        child_field_name_list = self.get_field_name_list_child_from_field_list(field_name_list.split(","))
        entity_list = []
        for index, candidate in enumerate(res["result"][self.entity]):
            entity_id = candidate["id"]
            entity = {**candidate}
            for child_field_name in child_field_name_list:
                _ = self.get_field_name_list_child_from_res(entity_id, self.entity, res["result"].get(child_field_name))
                entity[child_field_name] = _
            attachments = candidate.get("attachments") or None
            if attachments:
                pass
                attachments_info, status = await self.async_session.get(
                    url=f"{self.gle_user_config.apiServerHost}/rest/file/simple_list_with_ids",
                    gle_config=self.gle_user_config.dict(),
                    ssl=False,
                    params={
                        "fields": field_name_list,
                        "gql": f"id__s={attachments}"},
                    func=self.request_response_callback)
                entity["attachment"] = attachments_info['result']["attachment"]
                self.map_host_to_url(entity, self.gle_user_config.apiServerHost)
                for attachment in entity["attachment"]:
                    con, headers = await self.async_session.get(
                                    url=attachment["__download_oss_url"],
                                    ssl=False,
                                    func=self.request_file_response_callback,
                                    gle_config=self.gle_user_config.dict()
                                )
                    _, params = parse_header(headers.get("Content-Disposition"))
                    filename = unquote(params.get('filename'))
                    attachment["fileName"] = filename
                    attachment["fileContent"] = base64.b64encode(con).decode()
            entity_list.append(entity)
        return entity_list

    async def get_candidate_info(self, page: int, field_name_list: str):

        candidate_list = await self._get_candidate_info(page, field_name_list, check=False)
        return candidate_list

    async def get_max_page(self) -> int:

        field_name_list = ["id"]
        field_name_list = ",".join(field_name_list)
        info = await self._get_candidate_info(page=1, field_name_list=field_name_list, check=True)
        logger.info(info)
        i = BaseResponseModel(**info)
        logger.info("最大页数{}".format(i.totalpages))
        return i.totalpages

    async def initialize_field(self,
                  add_field_list: Optional[List[str]] = ["attachments", "tags","functions","industrys","locations"],
                  add_child_field_list: Optional[List[str]] = ["candidateexperience","candidatequalification","candidatelanguage","candidateproject"]):

        field_name_list = await self.get_field_name_list(self.entity)
        for _ in add_child_field_list:
            field_name_list_child = await self.get_field_name_list_child(_)
            field_name_list = field_name_list + field_name_list_child
        field_name_list = field_name_list + add_field_list
        field_name_list = list(set(field_name_list))

        logger.info(f"字段展示->{field_name_list}")

        field_name_list = ",".join(field_name_list)
        return field_name_list

    async def push_entity(self, entity: dict):
        logger.info(entity)
        client_list = entity.get("client", [])
        for client in client_list:
            client["type"] = "normal"
        info, status = await self.async_session.post(
            url=f"{self.gle_user_config.apiServerHost}/rest/{self.entity}/add",
            gle_config=self.gle_user_config.dict(),
            ssl=False,
            json=entity,
            func=self.request_response_callback)
        if info["status"] == True:
            logger.info(f"写回成功 id->{entity['id']}")
            logger.info(entity)
            return info
        else:
            logger.info(f"写回失败 id->{entity['id']} {info}")








if __name__ == '__main__':
    # asyncio.run(GleEntity(
    #     {
    #         "apiServerHost": "https://www.cgladvisory.com",
    #         "aesKey": "eae48bfe137cc656",
    #         "account": "system@wearecgl.com"
    #     }
    # ).run("candidate"))

    # recent = "1"
    # unit = "year"
    # asyncio.run(GleEntity(
    #     {
    #         "apiServerHost": "https://fsgtest.gllue.net",
    #         "aesKey": "824531e8cad2a287",
    #         "account": "api@fsg.com.cn"
    #     },
    #     {
    #         "entity": "candidate",
    #         "recent": recent,
    #         "unit": unit,
    #         "gql": None,
    #     }
    # ).run())

    recent = "1"
    unit = "year"
    asyncio.run(GleEntity(
        {
            "apiServerHost": "https://fsgtest.gllue.net",
            "aesKey": "824531e8cad2a287",
            "account": "api@fsg.com.cn"
        },
        {
            "entity": "candidate",
            "recent": recent,
            "unit": unit,
            "gql": None,
        }
    ).run())