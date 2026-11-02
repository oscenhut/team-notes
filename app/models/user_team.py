from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from .user import User
    from .team import Team

class UserTeam(Base):
    __tablename__ = "user_teams"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True)
    role: Mapped[str] = mapped_column(String, default="MEMBER", nullable=False)

    __table_args__ = (
        CheckConstraint("role IN ('OWNER', 'MEMBER')", name="check_user_team_role"),
    )

    # Relationships
    user: Mapped[User] = relationship("User", back_populates="user_teams")
    team: Mapped[Team] = relationship("Team", back_populates="user_teams")