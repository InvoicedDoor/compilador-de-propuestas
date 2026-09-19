from pydantic import Field, BaseModel

class ProjectRoleDto(BaseModel):
    code: str = Field(None)
    position: str = Field(None)