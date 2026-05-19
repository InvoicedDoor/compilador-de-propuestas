from __future__ import annotations
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import Integer, String

from .base import Base

class Rol(Base):
    __tablename__ = "roles_table"
    id: Mapped[int] = mapped_column(Integer,
                            primary_key=True,
                            autoincrement=True)
    rol: Mapped[str] = mapped_column(String(20))

    users: Mapped[list["User"]] = relationship(back_populates="rol")