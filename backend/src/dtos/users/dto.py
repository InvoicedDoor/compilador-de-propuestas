from pydantic import Field, BaseModel
from datetime import datetime
from typing import Optional

class UserDto(BaseModel):
    name: str = Field(None)
    first_lastname: str = Field(None)
    second_lastname: str = Field(None)
    regjster_on: datetime = Field(None)
    rol_id: int = Field(None)
    department: int = Field(None)

class UserFilterDto(UserDto):
    id: int = Field(None)
    active: bool = Field(None)

class RequesterUserDto(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    mail: str = Field(...)
    rol: int = Field(...)

class RegisterUserDto(BaseModel):
    name: str = Field(...)
    first_lastname: str = Field(...)
    second_lastname: Optional[str] = Field(None)
    rol_id: Optional[int] = Field(None)
