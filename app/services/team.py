from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.team import Team
from app.repositories.team import TeamRepository

class TeamService:
    def __init__(self, team_repo: Optional[TeamRepository] = None):
        self.team_repo = team_repo or TeamRepository()

    def create_team(self, db: Session, name: str) -> Team:
        """Business logic for creating a new team."""
        return self.team_repo.create(db, name=name)

    def get_team_by_id(self, db: Session, team_id: int) -> Team:
        """Retrieve a team by ID, raising 404 if not found."""
        team = self.team_repo.get(db, team_id)
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Team with id {team_id} not found"
            )
        return team

    def search_teams(self, db: Session, query_str: str, skip: int = 0, limit: int = 100) -> List[Team]:
        """Search teams matching the query string."""
        return self.team_repo.search(db, query_str=query_str, skip=skip, limit=limit)

    def update_team(self, db: Session, team_id: int, name: Optional[str] = None) -> Team:
        """Update team attributes, raising 404 if the team does not exist."""
        updated_team = self.team_repo.update(db, team_id, name=name)
        if not updated_team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Team with id {team_id} not found"
            )
        return updated_team