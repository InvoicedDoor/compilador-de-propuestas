from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class User(Base):
    __tablename__ = "users_table"

    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    
    name: Mapped[str] = mapped_column(String(100))

    first_lastname: Mapped[str] = mapped_column(String(40), nullable=False)

    second_lastname: Mapped[str] = mapped_column(String(40))
    
    rol_id: Mapped[int] = mapped_column(ForeignKey("roles_table.id"), default=2)

    rol: Mapped["Rol"] = relationship(
        "Rol",
        back_populates="users",
        lazy="joined"
    )

    credentials: Mapped["Auth"] = relationship(
        "Auth",
        back_populates="user",
        lazy="joined",
        uselist=False
    )

    user_proposal: Mapped[list["ProposalUsersModel"]] = relationship(
        "ProposalUsersModel",
        back_populates="users",
        lazy="joined"
    )

class RowUser(BaseModel):
    id: int = Field(None)
    mail: str = Field(None)
    rol: int = Field(None)

class RegisterUser(BaseModel):
    name: str = Field(...)
    first_lastname: str = Field(...)
    second_lastname: Optional[str] = Field(None)
    rol_id: Optional[int] = Field(None)