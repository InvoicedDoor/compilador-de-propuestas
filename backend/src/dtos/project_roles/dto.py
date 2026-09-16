from pydantic import Field, BaseModel

class ProjectRoleDto(BaseModel):
    id: str
    position: str