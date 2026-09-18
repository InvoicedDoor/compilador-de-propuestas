from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey
from typing import Optional

from ..base import Base

class ProjectFilesModel(Base):
    __tablename__ = "project_files_table"
    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project_table.id"), default=1)
    filename: Mapped[str | None] = mapped_column(String(50), nullable=True)
    path: Mapped[str | None] = mapped_column(String(50), nullable=True)
    code: Mapped[str] = mapped_column(String(70), nullable=False)
    file_type_id: Mapped[int] = mapped_column(ForeignKey("file_tipes_table.id"), default=1)
    active: Mapped[bool] = mapped_column(Boolean,default=True)

    project: Mapped["ProjectModel"] = relationship(back_populates="project_files") # type: ignore

    file_tipes: Mapped["FileTypeModel"] = relationship(back_populates="project_files") # type: ignore