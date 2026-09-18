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

    users: Mapped[list["UserModel"]] = relationship( # pyright: ignore[reportUndefinedVariable]
        "UserModel",
        back_populates="user_project",
        lazy="joined"
    )
    project: Mapped[list["ProjectModel"]] = relationship( # pyright: ignore
        back_populates="project_user",
        lazy="joined"
    )
    role: Mapped["ProjectRoleModel"] = relationship( # pyright: ignore[reportUndefinedVariable]
        back_populates="project_role",
        lazy="joined"
    )
    project_events: Mapped[list["ProjectEventModel"]] = relationship( # pyright: ignore[reportUndefinedVariable]
        back_populates="project_event",
        lazy="joined"
    )