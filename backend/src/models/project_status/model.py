from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey, UniqueConstraint
from typing import Optional

from ..base import Base

class ProjectStatusModel(Base):
    __tablename__ = "project_status"
    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(40), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False)

    project: Mapped[list["ProjectModel"]] = relationship(back_populates="status")  # type: ignore