from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey, UniqueConstraint
from typing import Optional

from ..base import Base

class FileTypeModel(Base):
    __tablename__ = "file_tipes_table"

    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    mime_type_id: Mapped[int] = mapped_column(ForeignKey("mime_tipes.id"))
    is_main_image: Mapped[bool] = mapped_column(Boolean(0))
    active: Mapped[bool] = mapped_column(Boolean(1))

    mime_type: Mapped["MimeTypeModel"] = relationship( # type: ignore
        back_populates="file_types"
    )