from __future__ import annotations
from pydantic import Field, BaseModel, model_validator
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey

from .base import Base

class Auth(Base):

    __tablename__ = "credentials_table"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users_table.id")
    )

    mail: Mapped[str] = mapped_column(
        String(100)
    )

    password: Mapped[str] = mapped_column(
        String(255)
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="credentials",
        lazy="joined"
    )

class GetAuth(BaseModel):
    id: int = Field(...)
    user_id: int = Field(...)
    mail: str = Field(...)
    password: str = Field(...)
    is_active: bool = Field(...)

class RegisterCredentials(BaseModel):
    mail: str = Field(...)
    password: str = Field(...)
    confirm_password: str = Field(...)
    
    @model_validator(mode="after")
    def validate_password(self):
        if self.password != self.confirm_password:
            raise ValueError("Las contraseñas no coinciden.")
        
        return self