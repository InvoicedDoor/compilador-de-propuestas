from .roles_dto import UserRol
from pydantic import Field, BaseModel
from typing import Optional
from config import ROLE_APPROVER_PROJECT

class ImageMetadata(BaseModel):
    id: int = Field(...)
    type: int = Field(...)
    name: str = Field(...)

class ProjectDto(BaseModel):
    project_title: str = Field(...)
    project_description: str = Field(...)
    project_manager: int = Field(...)
    images_metadata: Optional[list[ImageMetadata]] = None

class ProjectRol(BaseModel):
    id: str
    position: str

class ApproveProjectDto(BaseModel):
    approved: bool

class ProjectUsersFilter(BaseModel):
    id: int = Field(None)
    user_id: int = Field(None)
    project_role_id: int = Field(None)
    project_id: int = Field(None)
    active: bool = Field(None)

class ProjectUserDto(BaseModel):
    user_id: int = Field(None)
    project_role_id: int = Field(None)
    project_id: int = Field(None)
    active: bool = Field(None)

class ValidationUserRoleDto(BaseModel):
    user_id: int
    project_id: int
    project_roles: list[str]

class UpdateProjectUserDto(BaseModel):
    user_ids: list[int] = Field(None)
    project_role_id: int = Field(None)
    project_id: int = Field(None)
    active: bool = Field(None)

class ProjectUserResDto(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    position: ProjectRol = Field(...)
    rol: UserRol = Field(...)

class DeleteProjectFileDto(BaseModel):
    project: int = Field(...)
    file: int = Field(...)

class ProjectEventDto(BaseModel):
    user_id: int = Field(None)
    status_code: str = Field(None)
    project_id: int = Field(None)
    approved: bool = Field(None)
    active: bool = Field(None)

class ProjectEventStatusDto(BaseModel):
    project_id: int
    status_code: str
    approver_roles: list[str]
    project_role_status_code: list[str] = ROLE_APPROVER_PROJECT

class ProjectFilter(BaseModel):
    id: Optional[int] = Field(None)
    title: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    active: Optional[bool] = Field(None)

class ProjectFilesDto(BaseModel):
    project_id: int = Field(...)
    filename: str = Field(...)
    path: str = Field(...)
    code: str = Field(...)
    file_type_id: int = Field(...)

class ProjectFilesFilter(BaseModel):
    id: Optional[int] = Field(None)
    project_id: int = Field(...)
    filename: str = Field(...)
    path: str = Field(...)
    file_type_id: int = Field(...)
    active: Optional[bool] = Field(None)