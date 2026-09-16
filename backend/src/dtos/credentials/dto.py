from pydantic import Field, BaseModel
from datetime import datetime

class CredentialDto(BaseModel):
    user_id: int = Field(...)
    mail: str = Field(...)
    password: bool = Field(...)
    last_updated: datetime = Field(...)
    active: bool = Field(...)

class CredentialFilterDto(BaseModel):
    user_id: int = Field(None)
    mail: str = Field(None)
    active: bool = Field(None)