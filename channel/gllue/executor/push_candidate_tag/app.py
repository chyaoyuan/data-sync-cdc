import asyncio
import json
import re
from typing import Optional
import aiohttp
from loguru import logger
from aiohttp import ClientSession
from pydantic import BaseModel
import jmespath
from typing import List, Optional

from pydantic import BaseModel, Field


class ExtractBodyModel(BaseModel):
    texts: List[str]
    field: Optional[str] = Field(default="description")
    domain: Optional[str] = Field(default="hr")
    output_category: str
    top_k: Optional[int] = Field(default=1)


class ExpandBodyModel(BaseModel):
    texts: List[str]
    field: Optional[str] = Field(default="description")
    domain: Optional[str] = Field(default="hr")
    output_category: str
    top_k: Optional[int] = Field(default=1)
    recall_top_k: Optional[int] = Field(default=10)
    rerank: Optional[bool] = Field(default=False)
    timeout: Optional[int] = Field(default=20)


class Settings(BaseModel):
    TipTagServerHost: str


class TipTagApp:

    def __init__(self, session: ClientSession, settings: dict):
        self.session = session
        self.settings = Settings(**settings)

    def replace_symbols_with_hash(self, text):
        # 使用正则表达式将所有符号替换为#
        cleaned_text = re.sub(r'[^\w\s]', '#', text)
        cleaned_text = cleaned_text.replace("\n","###")
        return cleaned_text

    def process_dict(self, input_dict):
        if isinstance(input_dict, dict):
            processed_dict = {}
            for key, value in input_dict.items():
                processed_value = self.process_dict(value)# 递归处理字典的值
                processed_dict[key] = self.replace_symbols_with_hash(processed_value)
            return processed_dict
        elif isinstance(input_dict, list):
            processed_list = []
            for item in input_dict:
                processed_item = self.process_dict(item) # 递归处理列表中的元素
                processed_list.append(processed_item)
            return processed_list
        elif isinstance(input_dict, str):
            # .replace("\n","#")
            return self.replace_symbols_with_hash(input_dict)
        else:
            return input_dict

    async def extract(self, data: dict):
        url = f"{self.settings.TipTagServerHost}/v1/extract/tags"

        res = await self.session.post(url, json=ExtractBodyModel(**data).dict(), ssl=False)
        if res.status == 200:
            info = await res.json()
            return info, res.status
        info = await res.text()
        return info, res.status

    async def expand(self, data: dict):
        url = f"{self.settings.TipTagServerHost}/v1/expand/expand"
        res = await self.session.post(url, json=ExtractBodyModel(**data).dict(), ssl=False)
        if res.status == 200:
            info = await res.json()
            return info, res.status
        info = await res.text()
        return info, res.status

    async def extract_flatten(self, data, source: Optional[dict] = None, jme_s_path_list:Optional[list] = None):
        texts = []
        if source and jme_s_path_list:
            for path_gma in jme_s_path_list:
                if text := jmespath.search(path_gma, source):
                    texts.append(text)
            data["texts"] = [",".join(texts)]

        if source and not texts:
            return None
        url = f"{self.settings.TipTagServerHost}/v1/extract/tags"
        res = await self.session.post(url, json=ExtractBodyModel(**data).dict(), ssl=False,timeout=aiohttp.ClientTimeout(total=120))
        if res.status == 200:
            info = await res.json()
            tag_list = []
            for tags in info["tags"]:
                for tag in tags:
                    tag_list.append(tag)
            return tag_list


        logger.error(f"extract_error->{res.status} {await res.text()}")
        raise Exception(f"extract_error->{res.status} {await res.text()}")


    async def expand_flatten(self, data: dict):
        url = f"{self.settings.TipTagServerHost}/v1/expand/expand"
        _data = ExpandBodyModel(**data).dict()
        res = await self.session.post(url,
                                      json=_data,
                                      ssl=False,
                                      timeout=aiohttp.ClientTimeout(total=60))
        if res.status == 200:
            info = await res.json()
            tag_list = []
            for tags in info["tags"]:
                for tag in tags:
                    tag_list.append(tag)
            return tag_list
        logger.error(f"expand_error->{res.status} {await res.text()}")
        raise Exception(f"expand_error->{res.status} {await res.text()}")





