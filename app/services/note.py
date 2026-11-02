from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.note import Note
from app.repositories.note import NoteRepository

class NoteService:
    def __init__(self, note_repo: Optional[NoteRepository] = None):
        self.note_repo = note_repo or NoteRepository()

    def create_note(
        self, 
        db: Session, 
        *, 
        owner_user_id: int, 
        text: str, 
        visibility: str = "TEAM", 
        team_id: Optional[int] = None
    ) -> Note:
        """Business logic to create a new note."""
        return self.note_repo.create(
            db, 
            owner_user_id=owner_user_id, 
            text=text, 
            visibility=visibility, 
            team_id=team_id
        )

    def get_note(self, db: Session, note_id: int, current_user_id: Optional[int] = None) -> Note:
        """Retrieve a note by ID, enforcing multi-tenant isolation and visibility rules."""
        note = self.note_repo.get(db, note_id)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Note with id {note_id} not found"
            )
        
        # Enforce multi-tenant access control for private notes
        if note.visibility == "PRIVATE" and current_user_id and note.owner_user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this private note"
            )
            
        return note

    def search_notes(
        self, 
        db: Session, 
        *, 
        user_id: Optional[int] = None, 
        team_id: Optional[int] = None, 
        query_str: Optional[str] = None, 
        visibility: Optional[str] = None, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Note]:
        """Search and filter notes."""
        return self.note_repo.search(
            db, 
            user_id=user_id, 
            team_id=team_id, 
            query_str=query_str, 
            visibility=visibility, 
            skip=skip, 
            limit=limit
        )

    def update_note(
        self, 
        db: Session, 
        note_id: int, 
        *, 
        text: Optional[str] = None, 
        visibility: Optional[str] = None, 
        team_id: Optional[int] = None
    ) -> Note:
        """Update an existing note, raising 404 if not found."""
        updated_note = self.note_repo.update(
            db, 
            note_id, 
            text=text, 
            visibility=visibility, 
            team_id=team_id
        )
        if not updated_note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Note with id {note_id} not found"
            )
        return updated_note

    def delete_note(self, db: Session, note_id: int) -> None:
        """Delete a note, raising 404 if not found."""
        success = self.note_repo.delete(db, note_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Note with id {note_id} not found"
            )