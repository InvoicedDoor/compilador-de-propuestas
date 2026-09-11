from pydantic import Field, BaseModel
from typing import Optional

class UserRol(BaseModel):
    rol: str

class ProjectRol(BaseModel):
    code: str = Field(None)
    active: bool = Field(None)
