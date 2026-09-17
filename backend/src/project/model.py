from __future__ import annotations
from pydantic import Field, BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey
from typing import Optional

from src.models import Base

class ProjectModel(Base):
    __tablename__ = "project_table"
    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    main_directory: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status_id: Mapped[int] = mapped_column(ForeignKey("project_status.id"), default=1)
    active: Mapped[bool] = mapped_column(Boolean,default=True)

    project_files: Mapped[list["ProjectFilesModel"]] = relationship(back_populates="project") # pyright: ignore[reportUndefinedVariable]
    project_user: Mapped[list["ProjectUsersModel"]] = relationship(back_populates="project") # pyright: ignore[reportUndefinedVariable]
    status: Mapped["ProjectStatusModel"] = relationship(back_populates="project") #pyright: ignore[reportUndefinedVariable]