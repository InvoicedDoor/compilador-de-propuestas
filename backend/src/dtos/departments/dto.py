from pydantic import Field, BaseModel
from typing import Optional

class DepartmentDto(BaseModel):
    code: str = Field(None)
    description: bool = Field(None)
    active: bool = Field(None)