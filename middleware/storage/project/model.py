from typing import Optional, List
from typing_extensions import Literal
from pydantic import BaseModel, Field
from utils.data_processing_util import get_random_color_code


class ProjectFlowStage(BaseModel):
    name: str = Field(..., description="名字", example="搞毛")
    editable: bool = Field(default=False, description="是否可编辑", example=False)
    color: str = Field(default_factory=get_random_color_code, description="颜色 可以直接默认生成", example="#7B68EE")
    category: Literal['success', 'active', 'fail'] = Field(default="active", description="分类", example="active")


class ProjectBody(BaseModel):
    name: str = Field(..., description="project name", example="xxx")
    projectId: str = Field(..., description="project id", example="xxx")
    channelId: str = Field(..., description="channel id, project创建在哪个channel下")
    jobId: Optional[str] = Field(..., description="job id", example="xxx")
    flowStages: List[ProjectFlowStage] = Field(default=None, description="流程自定义模板")


class ProjectFlowStageBody(BaseModel):
    projectId: str = Field(..., description="project id", example="xxx")
    flowStages: List[ProjectFlowStage] = Field(..., description="流程自定义模板")
