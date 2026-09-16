from __future__ import annotations
from pydantic import Field, BaseModel, model_validator
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey

from .base import Base

class GetAuth(BaseModel):
    id: int = Field(...)
    user_id: int = Field(...)
    mail: str = Field(...)
    password: str = Field(...)
    active: bool = Field(...)

class RegisterCredentials(BaseModel):
    mail: str = Field(...)
    password: str = Field(...)
    confirm_password: str = Field(...)
    
    @model_validator(mode="after")
    def validate_password(self):
        if self.password != self.confirm_password:
            raise ValueError("Las contraseñas no coinciden.")
        
        return self