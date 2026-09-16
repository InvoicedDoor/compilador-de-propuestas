from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, ForeignKey, UniqueConstraint

from ..base import Base

class ProjectEventModel(Base):
    __tablename__ = "project_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users_table.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("project_table.id"))
    status_code: Mapped[str] = mapped_column(String(30))
    approved: Mapped[bool] = mapped_column(Boolean, default=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped["User"] = relationship( # pyright: ignore[reportUndefinedVariable]
        "User",
        back_populates="user_event",
        lazy="joined"
    )
    project: Mapped["Project"] = relationship( # type: ignore
        "Project",
        back_populates="project_event",
        lazy="joined"
    )

    uq_user_status = UniqueConstraint(user_id, project_id, status_code)