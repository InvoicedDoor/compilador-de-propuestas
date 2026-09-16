from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Boolean, Text, ForeignKey

from ..base import Base


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
    project: Mapped[list["Project"]] = relationship( # pyright: ignore
        "Project",
        back_populates="project_user",
        lazy="joined"
    )
    role: Mapped["ProjectRoleModel"] = relationship( # pyright: ignore[reportUndefinedVariable]
        back_populates="project_role",
        lazy="joined"
    )