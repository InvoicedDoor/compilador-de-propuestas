from __future__ import annotations
from pydantic import Field, BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey
from typing import Optional

from .base import Base

class Project(Base):
    __tablename__ = "project_table"
    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    main_directory: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status_id: Mapped[int] = mapped_column(ForeignKey("project_status.id"), default=1)
    active: Mapped[bool] = mapped_column(Boolean,default=True)

    project_files: Mapped[list["ProjectFilesModel"]] = relationship(back_populates="project")
    project_user: Mapped[list["ProjectUsersModel"]] = relationship(back_populates="project")
    project_event: Mapped[list["ProjectEventModel"]] = relationship(
        back_populates="project",
        lazy="joined"   
    )
    status: Mapped["ProjectStatusModel"] = relationship(back_populates="project")


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

    project: Mapped["Project"] = relationship(back_populates="project_files")



class ProjectStatusModel(Base):
    __tablename__ = "project_status"
    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(40), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False)

    project: Mapped[list["Project"]] = relationship(back_populates="status")

    action_event: Mapped["ProjectEventModel"] =  relationship(
        back_populates="action",
        lazy="joined"
    )


class ProjectUsersModel(Base):
    __tablename__ = "project_users_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users_table.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("project_table.id"))
    project_role_id: Mapped[int] = mapped_column(ForeignKey("project_roles_table.id"))
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    users: Mapped[list["User"]] = relationship( # pyright: ignore[reportUndefinedVariable]
        "User",
        back_populates="user_project",
        lazy="joined"
    )
    project: Mapped[list["Project"]] = relationship(
        "Project",
        back_populates="project_user",
        lazy="joined"
    )
    role: Mapped["ProjectRoleModel"] = relationship( # pyright: ignore[reportUndefinedVariable]
        back_populates="project_role",
        lazy="joined"
    )

class ProjectEventModel(Base):
    __tablename__ = "project_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users_table.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("project_table.id"))
    action_id: Mapped[int] = mapped_column(ForeignKey("project_status.id"))
    approved: Mapped[bool] = mapped_column(Boolean, default=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped["User"] = relationship( # pyright: ignore[reportUndefinedVariable]
        "User",
        back_populates="user_event",
        lazy="joined"
    )
    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="project_event",
        lazy="joined"
    )
    action: Mapped["ProjectStatusModel"] = relationship(
        back_populates="action_event",
        lazy="joined"
    )