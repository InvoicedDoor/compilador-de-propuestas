from pydantic import Field, BaseModel
from typing import Optional

class ImageMetadata(BaseModel):
    file_type: int = Field(...)
    file_name: str = Field(...)

class ProposalDto(BaseModel):
    proposal_title: str = Field(...)
    proposal_description: str = Field(...)
    proposal_manager: int = Field(...)
    images_metadata: Optional[list[ImageMetadata]] = None
