from typing import List, Optional, Literal

from pydantic import BaseModel, Field


class Config(BaseModel):
    traceId: int
    step: int
    end: Optional[bool] = Field(default=False)


class ExtractConfig(Config):
    jmespath: List[str]
    name: str


class OutPutGleMap(BaseModel):
    traceId: int
    gllueFieldName: List[str]


class ExtractModel(BaseModel):

    config: List[ExtractConfig]
    outPutGleMap: List[OutPutGleMap]


class ExpandConfig(Config):
    expandCategory: str


class ExpandModel(BaseModel):
    config: List[ExpandConfig]
    outPutGleMap: Optional[List[OutPutGleMap]]


class FuncConfig(Config):
    func: str


class FuncModel(BaseModel):
    config: List[FuncConfig]
    outPutGleMap: Optional[List[OutPutGleMap]]


class Settings(BaseModel):
    extract: ExtractModel
    expand: ExpandModel
    func: FuncModel
