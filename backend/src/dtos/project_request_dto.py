from .project_dto import UpdateProjectUserDto
from pydantic import BaseModel

class ProjectUserRequestBody(BaseModel):
    users: list[UpdateProjectUserDto]

class UpdateProjectStatusBody(BaseModel):
    status: str

class DeleteProjectUsersDto(BaseModel):
    user_id: int

class DeleteProjectUsersBody(BaseModel):
    users: list[DeleteProjectUsersDto]