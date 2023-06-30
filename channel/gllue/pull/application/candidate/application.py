import asyncio
import time

from loguru import logger

from channel.gllue.pull.application.schema.application import GleSchema
from channel.gllue.pull.application.base.model import BaseResponseModel


class GleCandidate(GleSchema):
    # 每页最大条数
    total_count: int = 100

    def __init__(self, gle_user_config: dict):
        super().__init__(gle_user_config)
        self.b = []
        self.url = []

    async def _get_candidate_info(self, page: int, field_name_list: str):
        res, status = await self.async_session.get(
            url="https://www.cgladvisory.com/rest/candidate/simple_list_with_ids",
            gle_config=self.gle_user_config.dict(),
            ssl=False,
            params={"fields": field_name_list,
                    "ordering": "-lastUpdateDate",
                    "paginate_by": self.total_count,
                    'page': page,
                    # 'gql': "lastUpdateDate__today"
                    'gql': "jobsubmission_set__cvsent_set__date__isnull|(mobile__isnull&has_attachment__eq=1&note_set__isnull=&tags__isnull)",
                    },
            func=self.request_response_callback)
        child_name_list = self.get_field_name_list_child_from_field_list(field_name_list.split(","))
        for index, candidate in enumerate(res["result"]["candidate"]):
            _id = candidate["id"]
            attachments = candidate.get("attachments") or None
            logger.info(f"attachment_id->{_id}")
            if attachments:
                res, status = await self.async_session.get(
                    url=f"https://www.cgladvisory.com/rest/file/simple_list_with_ids",
                    gle_config=self.gle_user_config.dict(),
                    ssl=False,
                    params={
                        "fields": field_name_list,
                        "gql": f"id__s={attachments}"},
                    func=self.request_response_callback)
                url_res = [self.gle_user_config.apiServerHost + _["__download_oss_url"] for _ in res["result"]['attachment']]

                if len(url_res) > 0:
                    con, headers = await self.async_session.get(
                        url=url_res[0],
                        ssl=False,
                        func=self.request_file_response_callback,
                        gle_config=self.gle_user_config.dict()
                    )
                    file_name = headers.get("Content-Disposition").split(".")[-1].replace('"', "")
                    with open(f"/Users/chenjiabin/Project/data-sync-cdc/channel/gllue/pull/data/{_id}.{file_name}", "wb") as f:
                        f.write(con)
                    logger.info(f"attachment->{_id}.{file_name}")
        return res

    async def get_candidate_info(self, page: int, field_name_list: str):

        candidate_list = await self._get_candidate_info(page, field_name_list)
        logger.info(candidate_list)
        logger.info(f"获取到第{page}页")

    async def get_max_page(self) -> int:

        field_name_list = ["id"]
        field_name_list = ",".join(field_name_list)
        info = await self._get_candidate_info(page=1, field_name_list=field_name_list)
        i = BaseResponseModel(**info)
        logger.info("最大页数{}".format(i.totalpages))
        return i.totalpages

    async def run(self):
        # await self.check_token()
        # field_name_list = await self.get_field_name_list("Candidate")
        # candidate_education_field_name_list = await self.get_field_name_list_child("candidateeducation")
        # field_name_list = field_name_list + candidate_education_field_name_list
        field_name_list = ['id', 'type', 'is_mpc', 'mpcDate', 'js_is_locked', 'owner', 'source', 'channel', 'englishName', 'chineseName', 'gender', 'dateOfBirth', 'address', 'mobile', 'mobile1', 'mobile2', 'mobile_prefix', 'mobile1_prefix', 'mobile2_prefix', 'email', 'email1', 'email2', 'wechat', 'stature', 'birth_place', 'ethnic', 'nationality', 'employment_type', 'desired_company', 'marital_status', 'notice_period', 'lastContactDate', 'dateAdded', 'latest_action', 'lastContactBy', 'status', 'lastUpdateStatusDate', 'annualSalary', 'expected_salary', 'is_deleted', 'recommend_user', 'built_in_self_assessment', 'built_in_expected_industry', 'built_in_expected_function', 'company', 'title', 'jobsubmission_count', 'highest_education', 'idCardType', 'idCardNo', 'virtual_mobile', 'authorization_status', 'parent', 'is_parent', 'lastUpdateDate', 'addedBy', 'lastUpdateBy', 'current_salary', 'gllueext_FreshGraduates', 'gllueext_native_place', 'id_card', 'political_status', 'candidateeducation_set__id', 'candidateeducation_set__start', 'candidateeducation_set__end', 'candidateeducation_set__school', 'candidateeducation_set__major', 'candidateeducation_set__location', 'candidateeducation_set__academy', 'candidateeducation_set__gpa', 'candidateeducation_set__description', 'candidateeducation_set__is_recent', 'candidateeducation_set__is_full_time', 'candidateeducation_set__degree', 'candidateeducation_set__gllueext_full_day']

        max_page: int = await self.get_max_page()

        logger.info(f"字段展示->{field_name_list}")
        field_name_list.append("attachments")
        field_name_list.append("tags")
        field_name_list = list(set(field_name_list))
        field_name_list = ",".join(field_name_list)
        # await asyncio.gather(
        #     *[
        #         self._get_candidate_info(page=_, field_name_list=field_name_list) for _ in range(1, max_page+1)
        #     ]
        # )
        for index_page in range(1, max_page+1):
            await self._get_candidate_info(page=index_page, field_name_list=field_name_list)
            logger.info(f"第{index_page}页")




if __name__ == '__main__':
    asyncio.run(GleCandidate(
        {
            "apiServerHost": "https://www.cgladvisory.com",
            "aesKey": "eae48bfe137cc656",
            "account": "system@wearecgl.com"
        }
    ).run())
    # asyncio.run(GleCandidate(
    #     {
    #         "apiServerHost": "https://fsgtest.gllue.net",
    #         "aesKey": "824531e8cad2a287",
    #         "account": "api@fsg.com.cn"
    #     }
    # ).run())