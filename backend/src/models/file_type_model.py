from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Boolean

from .base import Base

class MimeCategoryModel(Base):
    __tablename__ = "mime_category"
    id: Mapped[int] = mapped_column(Integer,
                                      primary_key=True,
                                      autoincrement=True)
    name: Mapped[str] = mapped_column(String(20),
                                      unique=True)
    
    # mime_type:  Mapped["MimeTypeExtensionTable"] = relationship(
    #     back_populates="category"
    # )

class MimeTypeModel(Base):
    __tablename__ = "mime_tipes"
    id: Mapped[int] = mapped_column(Integer,
                                      primary_key=True,
                                      autoincrement=True)
    mime_pattern: Mapped[str] = mapped_column(String(30))
    icon: Mapped[str] = mapped_column(String(50))
    category_id: Mapped[int] = mapped_column(Integer)
    # category_id: Mapped[int] = mapped_column(ForeignKey("mime_category.id"))

    mime_type_extension: Mapped[list["MimeTypeExtensionTable"]] = relationship(
        back_populates="mime_type"
    )
    # category: Mapped[list["MimeCategoryModel"]] = relationship(
        # back_populates="mime_type"
    # )

class ExtensionFile(Base):
    __tablename__ = "extension_file"
    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    extension: Mapped[str] = mapped_column(String(15),
                                           nullable=False,
                                           unique=True)
    
    mime_type_extension: Mapped[list["MimeTypeExtensionTable"]] = relationship(
        back_populates="extension"
    )
    

class MimeTypeExtensionTable(Base):
    __tablename__ = "mime_type_extension_table"
    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    extension_id: Mapped[int] = mapped_column(ForeignKey("extension_file.id"))
    mime_type_id: Mapped[int] = mapped_column(ForeignKey("mime_tipes.id"))
    
    mime_type: Mapped["MimeTypeModel"] = relationship(
        back_populates="mime_type_extension"
    )

    extension: Mapped["ExtensionFile"] = relationship(
        back_populates="mime_type_extension"
    )

    file_type: Mapped[list["FileTypeModel"]] = relationship(
        back_populates="mime_type_extension"
    )

class FileTypeModel(Base):
    __tablename__ = "file_tipes_table"

    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    mime_type_id: Mapped[int] = mapped_column(ForeignKey("mime_type_extension_table.id"))
    is_main_image: Mapped[bool] = mapped_column(Boolean(0))
    active: Mapped[bool] = mapped_column(Boolean(1))

    mime_type_extension: Mapped["MimeTypeExtensionTable"] = relationship(
        back_populates="file_type"
    )