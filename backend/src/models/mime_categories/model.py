from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey, UniqueConstraint
from typing import Optional

from ..base import Base

class MimeCategoryModel(Base):
    __tablename__ = "mime_category"
    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(String(20),unique=True)

    mime_tipes: Mapped[list["MimeTypeModel"]] = relationship( # type: ignore
        back_populates="mime_category"
    )