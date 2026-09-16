from pydantic import Field, BaseModel
from typing import Optional
from config import ROLE_APPROVER_PROJECT

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

class ApproveProjectDto(BaseModel):
    approved: bool