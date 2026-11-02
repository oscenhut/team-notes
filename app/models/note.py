from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Integer, String, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from .user import User
    from .team import Team

class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    owner_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    team_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("teams.id", ondelete="SET NULL"), nullable=True, index=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    visibility: Mapped[str] = mapped_column(String, default="TEAM", nullable=False)

    __table_args__ = (
        CheckConstraint("visibility IN ('PRIVATE', 'TEAM', 'PUBLIC')", name="check_note_visibility"),
    )

    # Relationships
    owner: Mapped[User] = relationship("User", back_populates="notes")
    team: Mapped[Optional[Team]] = relationship("Team", back_populates="notes")