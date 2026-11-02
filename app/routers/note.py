from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.services.note import NoteService

router = APIRouter(prefix="/notes", tags=["Notes"])

def get_note_service() -> NoteService:
    return NoteService()


@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    note_in: NoteCreate,
    owner_user_id: int = Query(..., description="ID of the user creating/owning the note"),
    db: Session = Depends(get_db),
    note_service: NoteService = Depends(get_note_service)
):
    """Create a new note with specified visibility and optional team association."""
    return note_service.create_note(
        db,
        owner_user_id=owner_user_id,
        text=note_in.text,
        visibility=note_in.visibility,
        team_id=note_in.team_id
    )


@router.get("", response_model=List[NoteResponse])
def search_notes(
    user_id: Optional[int] = Query(None, description="Filter notes by owner user ID"),
    team_id: Optional[int] = Query(None, description="Filter notes by team ID"),
    visibility: Optional[str] = Query(None, description="Filter by visibility ('PRIVATE', 'TEAM', 'PUBLIC')"),
    q: Optional[str] = Query(None, description="Search query string for note text content"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    note_service: NoteService = Depends(get_note_service)
):
    """Search and filter notes across users, teams, visibility levels, and text keywords."""
    return note_service.search_notes(
        db,
        user_id=user_id,
        team_id=team_id,
        query_str=q,
        visibility=visibility,
        skip=skip,
        limit=limit
    )


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    note_service: NoteService = Depends(get_note_service)
):
    """Retrieve a specific note by its ID."""
    return note_service.get_note(db, note_id=note_id)


@router.patch("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_in: NoteUpdate,
    db: Session = Depends(get_db),
    note_service: NoteService = Depends(get_note_service)
):
    """Update an existing note's text, visibility, or team link."""
    return note_service.update_note(
        db,
        note_id=note_id,
        text=note_in.text,
        visibility=note_in.visibility,
        team_id=note_in.team_id
    )


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    note_service: NoteService = Depends(get_note_service)
):
    """Delete a note by its ID."""
    note_service.delete_note(db, note_id=note_id)
    return None