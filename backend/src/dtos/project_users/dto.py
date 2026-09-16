from ..project_roles.dto import ProjectRoleDto
from ..company_roles.dto import UserRoleDto
from pydantic import Field, BaseModel

class ProjectUserDto(BaseModel):
    user_id: int = Field(None)
    project_role_id: int = Field(None)
    project_id: int = Field(None)
    active: bool = Field(None)

class ProjectUsersFilter(ProjectUserDto):
    id: int = Field(None)

class UpdateProjectUserDto(BaseModel):
    user_ids: list[int] = Field(None)
    project_role_id: int = Field(None)
    project_id: int = Field(None)
    active: bool = Field(None)

class ProjectUserResDto(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    position: ProjectRoleDto = Field(...)
    rol: UserRoleDto = Field(...)

class ProjectUserRequestBody(BaseModel):
    users: list[UpdateProjectUserDto]

class DeleteProjectUsersDto(BaseModel):
    user_id: int

class DeleteProjectUsersBody(BaseModel):
    users: list[DeleteProjectUsersDto]

class DeleteProjectUserArgs(BaseModel):
    user: DeleteProjectUsersDto = Field(None)
    