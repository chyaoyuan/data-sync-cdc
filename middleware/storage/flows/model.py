from typing import List
from pydantic import BaseModel, Field


class FlowsBody(BaseModel):
    entityId: List[str] = Field(..., description="简历id, 可以直接多个", example=["xxx1", "xxx2"])
    projectId: str = Field(..., description="project id", example="xxx")
    stageName: str = Field(default="投递人选", description="stage的中文名, 无要求就直接用默认值就行", example="投递人选")
