from typing import List
from pydantic import BaseModel, Field


class RequestInfo(BaseModel):
    task_ids: List[str] = Field(..., description="task id set", example="xxx")
    data: List[dict] = Field(..., description="需要转换的数据", example="xxx")
    keep_all_src_fields: bool = Field(default=False, description="是否保留源数据", example="xxx")
