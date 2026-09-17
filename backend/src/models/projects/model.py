from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey
from typing import Optional

from ..base import Base

class ProjectModel(Base):
    __tablename__ = "project_table"
    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    main_directory: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status_id: Mapped[int] = mapped_column(ForeignKey("project_status.id"), default=1)
    active: Mapped[bool] = mapped_column(Boolean,default=True)

    project_files: Mapped[list["ProjectFilesModel"]] = relationship(back_populates="project") # type: ignore
    project_user: Mapped[list["ProjectUsersModel"]] = relationship(back_populates="project") # type: ignore

    status: Mapped["ProjectStatusModel"] = relationship(back_populates="project") # type: ignore

