from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

class UserModel(Base):
    __tablename__ = "users_table"

    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    
    name: Mapped[str] = mapped_column(String(100))

    first_lastname: Mapped[str] = mapped_column(String(40), nullable=False)

    second_lastname: Mapped[str] = mapped_column(String(40))
    
    company_role_id: Mapped[int] = mapped_column(ForeignKey("company_roles_table.id"), default=2)

    department_id: Mapped[int] = mapped_column(ForeignKey("departments_table.id"))

    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    role: Mapped["CompanyRoleModel"] = relationship( # pyright: ignore[reportUndefinedVariable]
        "CompanyRoleModel",
        back_populates="users",
        lazy="joined"
    )

    credentials: Mapped["Auth"] = relationship( # pyright: ignore[reportUndefinedVariable]
        "Auth",
        back_populates="user",
        lazy="joined",
        uselist=False
    )

    user_project: Mapped[list["ProjectUsersModel"]] = relationship( # pyright: ignore[reportUndefinedVariable]
        back_populates="users",
        lazy="joined"
    )

    department: Mapped["DepartmentModel"] = relationship( # pyright: ignore[reportUndefinedVariable]
            back_populates="users",
            lazy="joined"
        )
