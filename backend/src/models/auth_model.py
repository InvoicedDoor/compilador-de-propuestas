from pydantic import Field, BaseModel
from src.models.user_model import User

class Auth(BaseModel):
    id: int = Field(...)
    user: User = Field(...)
    mail: str = Field(...)
    password: str = Field(...)
    is_active: bool = Field(...)

class GetAuth(BaseModel):
    id: int = Field(...)
    user_id: int = Field(...)
    mail: str = Field(...)
    password: str = Field(...)
    is_active: bool = Field(...)

class RegisterCredentials(BaseModel):
    user_id: int = Field(...)
    mail: str = Field(...)
    password: str = Field(...)