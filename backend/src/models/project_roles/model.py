from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean

from ..base import Base

class ProjectRoleModel(Base):
    __tablename__ = "project_roles_table"
    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    code: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(40), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    project_role: Mapped["ProjectUsersModel"] = relationship(back_populates="role") # pyright: ignore[reportUndefinedVariable]