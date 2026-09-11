from __future__ import annotations
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import Integer, String, Boolean

from .base import Base

class Rol(Base):
    __tablename__ = "company_roles_table"
    id: Mapped[int] = mapped_column(Integer,
                            primary_key=True,
                            autoincrement=True)
    code: Mapped[str] = mapped_column(String(50))
    rol: Mapped[str] = mapped_column(String(20))

    users: Mapped[list["User"]] = relationship(back_populates="rol") # pyright: ignore[reportUndefinedVariable]

class ProjectRoleModel(Base):
    __tablename__ = "project_roles_table"
    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    code: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(40), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    project_role: Mapped["ProjectUsersModel"] = relationship(back_populates="role") # pyright: ignore[reportUndefinedVariable]