from __future__ import annotations
from typing import List, TYPE_CHECKING
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from .note import Note
    from .user_team import UserTeam

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    # Relationships
    notes: Mapped[List[Note]] = relationship("Note", back_populates="owner", cascade="all, delete-orphan")
    user_teams: Mapped[List[UserTeam]] = relationship("UserTeam", back_populates="user", cascade="all, delete-orphan")