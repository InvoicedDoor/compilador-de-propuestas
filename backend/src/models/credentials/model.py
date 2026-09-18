from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey, UniqueConstraint
from typing import Optional

from ..base import Base

class Auth(Base):

    __tablename__ = "credentials_table"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users_table.id"))

    mail: Mapped[str] = mapped_column(String(100))

    password: Mapped[str] = mapped_column(String(255))

    active: Mapped[bool] = mapped_column(Boolean,default=True)

    user: Mapped["UserModel"] = relationship( # type: ignore
        "UserModel",
        back_populates="credentials",
        lazy="joined"
    )
