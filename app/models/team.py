from __future__ import annotations
from typing import List, TYPE_CHECKING
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from .note import Note
    from .user_team import UserTeam

class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    # Relationships
    user_teams: Mapped[List[UserTeam]] = relationship("UserTeam", back_populates="team", cascade="all, delete-orphan")
    notes: Mapped[List[Note]] = relationship("Note", back_populates="team", cascade="all, delete-orphan")