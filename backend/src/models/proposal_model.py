from __future__ import annotations
from pydantic import Field, BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey
from typing import Optional

from .base import Base

class Proposal(Base):
    __tablename__ = "proposal_table"
    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(Text,
    nullable=True)
    active: Mapped[bool] = mapped_column(Boolean,default=True)

    proposal_files: Mapped[list["ProposalFiles"]] = relationship(back_populates="proposal")

    proposal_user: Mapped[list["ProposalUsersModel"]] = relationship(back_populates="proposal")

class ProposalFiles(Base):
    __tablename__ = "proposal_files_table"
    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    proposal_id: Mapped[int] = mapped_column(ForeignKey("proposal_table.id"))
    filename: Mapped[str] = mapped_column(String(50), nullable=False)
    path: Mapped[str] = mapped_column(String(50), nullable=False)
    file_type_id: Mapped[int] = mapped_column(ForeignKey("file_tipes_table.id"))
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    proposal: Mapped["Proposal"] = relationship(back_populates="proposal_files")


class ProposalUsersModel(Base):
    __tablename__ = "proposal_users_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users_table.id"))
    proposal_id: Mapped[int] = mapped_column(ForeignKey("proposal_table.id"))
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    users: Mapped[list["User"]] = relationship(
        "User",
        back_populates="user_proposal",
        lazy="joined"
    )
    proposal: Mapped[list["Proposal"]] = relationship(
        "Proposal",
        back_populates="proposal_user",
        lazy="joined"
    )

class ProposalFilter(BaseModel):
    id: Optional[int] = Field(None)
    title: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    active: Optional[bool] = Field(None)

class ProposalFilesDto(BaseModel):
    proposal_id: int = Field(...)
    filename: str = Field(...)
    path: str = Field(...)
    file_type_id: int = Field(...)

class ProposalFilesFilter(BaseModel):
    id: Optional[int] = Field(None)
    proposal_id: int = Field(...)
    filename: str = Field(...)
    path: str = Field(...)
    file_type_id: int = Field(...)
    active: Optional[bool] = Field(None)