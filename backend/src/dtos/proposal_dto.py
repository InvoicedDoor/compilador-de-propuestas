from pydantic import Field, BaseModel
from typing import Optional

class ImageMetadata(BaseModel):
    id: int = Field(...)
    type: int = Field(...)
    name: str = Field(...)

class ProposalDto(BaseModel):
    proposal_title: str = Field(...)
    proposal_description: str = Field(...)
    proposal_manager: int = Field(...)
    images_metadata: Optional[list[ImageMetadata]] = None

class UserRol:
    id: int
    rol: str

class ProposalUserDto:
    id: int
    name: str
    rol: UserRol
    active: bool

class DeleteProposalFileDto(BaseModel):
    proposal: int = Field(...)
    file: int = Field(...)