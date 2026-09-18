from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, ForeignKey, UniqueConstraint

from ..base import Base

class ProjectEventModel(Base):
    __tablename__ = "project_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_project_id: Mapped[int] = mapped_column(ForeignKey("project_users_table.id"))
    status_code: Mapped[str] = mapped_column(String(30))
    approved: Mapped[bool] = mapped_column(Boolean, default=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    project_event: Mapped["ProjectUsersModel"] = relationship( # pyright: ignore[reportUndefinedVariable]
        back_populates="project_events",
        lazy="joined"
    )

    uq_user_status = UniqueConstraint(user_project_id, status_code)