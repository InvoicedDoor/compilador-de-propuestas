from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey, UniqueConstraint
from typing import Optional

from ..base import Base

class CompanyRoleModel(Base):
    __tablename__ = "company_roles_table"
    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    rol: Mapped[str] = mapped_column(String(40), nullable=False)

    users: Mapped[list["UserModel"]] = relationship(back_populates="role") # pyright: ignore[reportUndefinedVariable]