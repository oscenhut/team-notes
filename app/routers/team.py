from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.team import TeamCreate, TeamUpdate, TeamResponse
from app.schemas.user_team import UserTeamCreate, UserTeamResponse
from app.services.team import TeamService
from app.services.user_team import UserTeamService

router = APIRouter(prefix="/teams", tags=["Teams"])

# Dependency providers
def get_team_service() -> TeamService:
    return TeamService()

def get_user_team_service() -> UserTeamService:
    return UserTeamService()


@router.post("", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(
    team_in: TeamCreate,
    db: Session = Depends(get_db),
    team_service: TeamService = Depends(get_team_service)
):
    """Create a new team."""
    return team_service.create_team(db, name=team_in.name)


@router.get("", response_model=List[TeamResponse])
def search_teams(
    q: Optional[str] = Query(None, description="Search query string for team name"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    team_service: TeamService = Depends(get_team_service)
):
    """Search or list teams."""
    if q:
        return team_service.search_teams(db, query_str=q, skip=skip, limit=limit)
    # Fallback or general listing using an empty or wildcard search
    return team_service.search_teams(db, query_str="", skip=skip, limit=limit)


@router.get("/{team_id}", response_model=TeamResponse)
def get_team(
    team_id: int,
    db: Session = Depends(get_db),
    team_service: TeamService = Depends(get_team_service)
):
    """Retrieve a specific team by ID."""
    return team_service.get_team_by_id(db, team_id=team_id)


@router.patch("/{team_id}", response_model=TeamResponse)
def update_team(
    team_id: int,
    team_in: TeamUpdate,
    db: Session = Depends(get_db),
    team_service: TeamService = Depends(get_team_service)
):
    """Update team details."""
    return team_service.update_team(db, team_id=team_id, name=team_in.name)


# --- Team Memberships ---

@router.get("/{team_id}/members", response_model=List[UserTeamResponse])
def get_team_members(
    team_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    team_team_service: UserTeamService = Depends(get_user_team_service)
):
    """List all members belonging to a team."""
    return team_team_service.get_team_members(db, team_id=team_id, skip=skip, limit=limit)


@router.post("/{team_id}/members", response_model=UserTeamResponse, status_code=status.HTTP_201_CREATED)
def add_team_member(
    team_id: int,
    membership_in: UserTeamCreate,
    db: Session = Depends(get_db),
    user_team_service: UserTeamService = Depends(get_user_team_service)
):
    """Add a user to a team with a specific role ('OWNER' or 'MEMBER')."""
    return user_team_service.add_user_to_team(
        db, 
        user_id=membership_in.user_id, 
        team_id=team_id, 
        role=membership_in.role
    )


@router.delete("/{team_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_team_member(
    team_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    user_team_service: UserTeamService = Depends(get_user_team_service)
):
    """Remove a user from a team."""
    user_team_service.remove_user_from_team(db, user_id=user_id, team_id=team_id)
    return None