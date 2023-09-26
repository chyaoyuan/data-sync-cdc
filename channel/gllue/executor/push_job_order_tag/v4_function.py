from typing import Optional, List

from loguru import logger
from pydantic import BaseModel, Field


class ValueModel(BaseModel):
    int_value: Optional[int] = Field(default=0)
    int_list_value: Optional[List[int]] = Field(default=[])
    float_value: Optional[float] = Field(default=0.0)
    float_list_value: Optional[List[int]] = Field(default=[])
    string_value: Optional[str] = Field(default=None)
    string_list_value: Optional[List[str]] = Field(default=None)


class RangeQueryModel(BaseModel):
    gte: Optional[ValueModel] = Field(default=None)
    lte: Optional[ValueModel] = Field(default=None)


class TermModel(BaseModel):
    term: Optional[ValueModel] = Field(default=None)


class SpanModel(BaseModel):
    entity: str
    range_query: Optional[RangeQueryModel] = Field(default=None)
    term_query: Optional[TermModel] = Field(default=None)


class FunctionV4ToGle:
    def __init__(self):
        self.gle_entity = {}

    def job_parse_v2_salary_range_query(self, range_query: dict):
        # 如果只解析出一个就补全
        range_query_obj = RangeQueryModel(**range_query)
        gte = range_query_obj.gte
        lte = range_query_obj.lte
        logger.info(self.gle_entity)
        if bool(gte) != bool(lte):
            self.gle_entity["monthlySalary"] = self.gle_entity["maxMonthlySalary"] = int(gte.float_value) if gte else int(lte.float_value)
        if gte and lte:
            self.gle_entity["monthlySalary"] = int(gte.float_value)
            self.gle_entity["maxMonthlySalary"] = int(lte.float_value)

    def job_parse_v2_work_year_term(self, term: dict):
        term_obj = ValueModel(**term)
        self.gle_entity["gllueext_work_cycle"] = term_obj.string_value

    def job_parse_v2_age_range_query(self, range_query: dict):
        range_query_obj = RangeQueryModel(**range_query)
        gte = range_query_obj.gte
        lte = range_query_obj.lte
        if bool(gte) != bool(lte):
            self.gle_entity["gllueext_number_1690859041960"] = self.gle_entity["gllueext_number_1690859067510"] = int(gte.float_value) if gte else int(lte.float_value)
        if gte:
            self.gle_entity["gllueext_number_1690859041960"] = int(gte.int_value)
        if lte:
            self.gle_entity["gllueext_number_1690859067510"] = int(lte.int_value)



