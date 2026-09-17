from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime, UniqueConstraint
from datetime import datetime

from ..base import Base

class ProjectEventModel(Base):
    __tablename__ = "project_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_project_id: Mapped[int] = mapped_column(ForeignKey("project_users_table.id"))
    status_code: Mapped[str] = mapped_column(String(30))
    realized_on: Mapped[datetime] = mapped_column(DateTime(True))
    approved: Mapped[bool] = mapped_column(Boolean, default=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    project_user: Mapped["ProjectUsersModel"] = relationship( # pyright: ignore[reportUndefinedVariable]
        "ProjectUsersModel",
        back_populates="project_user_event",
        lazy="joined"
    )

    uq_user_status = UniqueConstraint(user_project_id, status_code)