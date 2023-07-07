import asyncio

import requests
from loguru import logger

from channel.gllue.application.applicaiton import GlePullApplication


async def sync_candidate_pull_and_push():
    candidate_app = GlePullApplication({
                "apiServerHost": "https://fsgtest.gllue.net",
                "aesKey": "824531e8cad2a287",
                "account": "api@fsg.com.cn"
            }, {
                "entity": "client",
                "recent": "1",
                "unit": "year",
                "gql": None,
            }).candidate_app
    await candidate_app.check_token()
    field_name_list: str = await candidate_app.initialize_field()
    max_page_index = await candidate_app.get_max_page()

    for index_page in range(1, max_page_index + 1):
        entity_list = await candidate_app.get_candidate_info(index_page, field_name_list)
        logger.info(f"第{index_page}页 entity->{candidate_app.entity} id->{[entity['id'] for entity in entity_list]}")
        for entity in entity_list:
            gle_id = entity["id"]
            logger.info(entity)

                #         await candidate_app.push_entity(gle_entity)
                #     else:
                #         logger.error(f"未知解析错误 id->{gle_id} {res.status_code} {res.content}")
                # else:
                #     logger.info(f"解析错误 id->{gle_id} {res.status_code} {res.content}")
                #     logger.info(res.content)
                #     continue





if __name__ == '__main__':
    asyncio.run(sync_candidate_pull_and_push())

