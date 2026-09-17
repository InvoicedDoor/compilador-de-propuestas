from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, ForeignKey

from ..base import Base

class ProjectFilesModel(Base):
    __tablename__ = "project_files_table"
    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project_table.id"))
    filename: Mapped[str] = mapped_column(String(50), nullable=False)
    path: Mapped[str] = mapped_column(String(50), nullable=False)
    code: Mapped[str] = mapped_column(String(70), nullable=False)
    file_type_id: Mapped[int] = mapped_column(ForeignKey("file_tipes_table.id"))
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    project: Mapped["ProjectModel"] = relationship(back_populates="project_files") # type: ignore