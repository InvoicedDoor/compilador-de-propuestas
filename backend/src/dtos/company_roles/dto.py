from pydantic import Field, BaseModel, model_validator
from typing import Optional

class CompanyRoleDto(BaseModel):
    code: str
    rol: str

class CompanyRoleFilter(BaseModel):
    id: int = Field(None)
    code: str = Field(None)

    @model_validator(mode="after")
    def validate_fields(self):
        if not self.id and self.code:
            raise ValueError("Debe proporcionar un filtro.")

        return self

class UserRoleDto(BaseModel):
    rol: str

class ValidationUserRoleDto(BaseModel):
    user_id: int
    project_id: int
    project_roles: list[str]