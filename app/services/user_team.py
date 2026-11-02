from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user_team import UserTeam
from app.repositories.user_team import UserTeamRepository

class UserTeamService:
    def __init__(self, user_team_repo: Optional[UserTeamRepository] = None):
        self.user_team_repo = user_team_repo or UserTeamRepository()

    def add_user_to_team(self, db: Session, user_id: int, team_id: int, role: str = "MEMBER") -> UserTeam:
        """Business logic to add a user to a team with validation."""
        if role not in ("OWNER", "MEMBER"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role. Must be 'OWNER' or 'MEMBER'."
            )
        existing = self.user_team_repo.get(db, user_id, team_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already a member of this team."
            )
        return self.user_team_repo.add(db, user_id=user_id, team_id=team_id, role=role)

    def remove_user_from_team(self, db: Session, user_id: int, team_id: int) -> None:
        """Remove a user from a team, raising 404 if not found."""
        success = self.user_team_repo.remove(db, user_id, team_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Membership record not found."
            )

    def get_team_members(self, db: Session, team_id: int, skip: int = 0, limit: int = 100) -> List[UserTeam]:
        """Get all members of a team."""
        return self.user_team_repo.get_team_members(db, team_id=team_id, skip=skip, limit=limit)

    def get_user_teams(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[UserTeam]:
        """Get all teams a user belongs to."""
        return self.user_team_repo.get_user_teams(db, user_id=user_id, skip=skip, limit=limit)

    def update_member_role(self, db: Session, user_id: int, team_id: int, role: str) -> UserTeam:
        """Update a member's role."""
        if role not in ("OWNER", "MEMBER"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role. Must be 'OWNER' or 'MEMBER'."
            )
        membership = self.user_team_repo.update_role(db, user_id, team_id, role)
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Membership record not found."
            )
        return membership