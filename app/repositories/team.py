from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.team import Team

class TeamRepository:
    def create(self, db: Session, *, name: str) -> Team:
        """Create and persist a new team."""
        db_team = Team(name=name)
        db.add(db_team)
        db.commit()
        db.refresh(db_team)
        return db_team

    def get(self, db: Session, team_id: int) -> Optional[Team]:
        """Retrieve a team by its ID."""
        stmt = select(Team).where(Team.id == team_id)
        return db.scalars(stmt).first()

    def search(self, db: Session, query_str: str, skip: int = 0, limit: int = 100) -> List[Team]:
        """Search teams by name matching the query string."""
        search_pattern = f"%{query_str}%"
        stmt = (
            select(Team)
            .where(Team.name.ilike(search_pattern))
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(stmt).all())

    def update(self, db: Session, team_id: int, *, name: Optional[str] = None) -> Optional[Team]:
        """Update an existing team's details."""
        db_team = self.get(db, team_id)
        if not db_team:
            return None
        
        if name is not None:
            db_team.name = name
            
        db.commit()
        db.refresh(db_team)
        return db_team