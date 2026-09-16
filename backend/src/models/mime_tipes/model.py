from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey

from ..base import Base

class MimeTypeModel(Base):
    __tablename__ = "mime_tipes"
    id: Mapped[int] = mapped_column(Integer,
                                      primary_key=True,
                                      autoincrement=True)
    mime_pattern: Mapped[str] = mapped_column(String(30))
    icon: Mapped[str] = mapped_column(String(50))
    # category_id: Mapped[int] = mapped_column(Integer)
    extension: Mapped[str] = mapped_column(String(30), nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("mime_category.id"))

    file_types: Mapped[list["FileTypeModel"]] = relationship( # type: ignore
        back_populates="mime_type"
    )

    mime_category: Mapped["MimeCategoryModel"] = relationship( # type: ignore
        back_populates="mime_tipes"
    )