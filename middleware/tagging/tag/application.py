import asyncio
from typing import Type, Literal
from loguru import logger

from middleware.settings.settings import Settings
from middleware.tagging.base.application import BaseApplication


class TagApplication(BaseApplication):
    def __init__(self, settings: Type[Settings]):

        super().__init__(settings)

    async def un_repeat_tag(self, tag_list: list, kind: Literal["position3", "industry2"]):

        payload = {
            "texts": list(set(tag_list)),
            "field": "description" if kind == "position3" else "company",
            "domain": "hr",
            "output_category": kind,
            "top_k": 1
        }

        res, status = await self.session.post("http://effex.tpddns.cn:7777/v1alpha1/tagging/expand",ssl=False,json=payload,func=self.request_response_callback)
        # # {'tags': [[{'tag': '互联网/IT/电子/通信-电子商务', 'category': 'industry', 'score': 1.0}], [{'tag': '互联网/IT/电子/通信-互联网', 'category': 'industry', 'score': 1.0}]]}
        print(res)
        _tag_list = []
        if status == 200:
            # 无标签
            if not res.get("tags"):
                return
            for tag_info_list in res["tags"]:
                for tag_indo in tag_info_list:
                    _tag_list.append(tag_indo["tag"])
            logger.info(_tag_list)
            return list(set(_tag_list))
        else:
            logger.info(f"标签失败 {status} {res}")



if __name__ == '__main__':
    t = TagApplication(Settings).un_repeat_tag(tag_list=["阿里巴巴", '百度'], kind="industry2")
    i = asyncio.run(t)
    print(i)
