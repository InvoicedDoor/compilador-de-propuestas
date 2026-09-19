from ..project_roles.dto import ProjectRoleDto
from ..company_roles.dto import UserRoleDto
from pydantic import Field, BaseModel

class ProjectUserDto(BaseModel):
    user_id: int = Field(None)
    project_role_id: int = Field(None)
    project_id: int = Field(None)
    active: bool = Field(False)

class ProjectUsersFilter(ProjectUserDto):
    id: int = Field(None)

class ProjectUsersDto(BaseModel):
    user_ids: list[int] = Field(None)
    project_role_id: int = Field(None)
    project_id: int = Field(None)
    active: bool = Field(None)

class UpdateProjectUserRoleDto(BaseModel):
    user_id: int
    project_role: str

class AddProjectUsereDto(BaseModel):
    mail: str
    project_role: str
    
class ProjectUserResDto(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    position: ProjectRoleDto = Field(...)
    rol: UserRoleDto = Field(...)

class ProjectUserRequestBody(BaseModel):
    users: list[ProjectUsersDto]

class AddProjectUserRequestBody(BaseModel):
    users: list[AddProjectUsereDto]

class DeleteProjectUsersDto(BaseModel):
    user_id: int

class DeleteProjectUsersBody(BaseModel):
    users: list[DeleteProjectUsersDto]

class DeleteProjectUserArgs(BaseModel):
    user: DeleteProjectUsersDto = Field(None)
    