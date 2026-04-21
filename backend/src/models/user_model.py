from pydantic import BaseModel, Field
from .rol_model import Rol

class User(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    rol: Rol = Field(...)

class RowUser(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    rol_id: int = Field(...)

class RegisterUser(BaseModel):
    name: str = Field(...)
    rol_id: int = Field(...)