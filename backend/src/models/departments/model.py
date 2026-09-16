from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean
from ..base import Base

class DepartmentModel(Base):
    __tablename__ = "departments_table"
    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(60), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    department: Mapped[list["UserModel"]] = relationship(back_populates="role") # pyright: ignore[reportUndefinedVariable]