from pydantic import Field, BaseModel
from typing import Optional

class ImageMetadata(BaseModel):
    id: int = Field(...)
    type: int = Field(...)
    name: str = Field(...)

class ProjectDto(BaseModel):
    project_title: str = Field(...)
    project_description: str = Field(...)
    project_manager: int = Field(...)
    images_metadata: Optional[list[ImageMetadata]] = None

class ProjectFilter(BaseModel):
    id: Optional[int] = Field(None)
    title: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    active: Optional[bool] = Field(None)