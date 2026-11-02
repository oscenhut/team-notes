from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user_team import UserTeam

class UserTeamRepository:
    def add(self, db: Session, *, user_id: int, team_id: int, role: str = "MEMBER") -> UserTeam:
        """Add a user to a team with a specific role."""
        db_membership = UserTeam(user_id=user_id, team_id=team_id, role=role)
        db.add(db_membership)
        db.commit()
        db.refresh(db_membership)
        return db_membership

    def get(self, db: Session, user_id: int, team_id: int) -> Optional[UserTeam]:
        """Retrieve a specific team membership record."""
        stmt = select(UserTeam).where(UserTeam.user_id == user_id, UserTeam.team_id == team_id)
        return db.scalars(stmt).first()

    def remove(self, db: Session, user_id: int, team_id: int) -> bool:
        """Remove a user from a team."""
        membership = self.get(db, user_id, team_id)
        if not membership:
            return False
        db.delete(membership)
        db.commit()
        return True

    def get_team_members(self, db: Session, team_id: int, skip: int = 0, limit: int = 100) -> List[UserTeam]:
        """List all memberships for a given team."""
        stmt = select(UserTeam).where(UserTeam.team_id == team_id).offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    def get_user_teams(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[UserTeam]:
        """List all team memberships for a given user."""
        stmt = select(UserTeam).where(UserTeam.user_id == user_id).offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    def update_role(self, db: Session, user_id: int, team_id: int, role: str) -> Optional[UserTeam]:
        """Update a member's role within a team."""
        membership = self.get(db, user_id, team_id)
        if not membership:
            return None
        membership.role = role
        db.commit()
        db.refresh(membership)
        return membership