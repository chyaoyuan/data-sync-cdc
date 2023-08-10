from pydantic import BaseModel, Field


class ChannelBody(BaseModel):
    channelId: str = Field(..., description="channel id", example="xxx")
    spaceId: str = Field(..., description="space id", example="xxx")
    name: str = Field(..., description="channel name", example="呵呵")
