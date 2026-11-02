from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, or_

from app.models.note import Note

class NoteRepository:
    def create(
        self, 
        db: Session, 
        *, 
        owner_user_id: int, 
        text: str, 
        visibility: str = "TEAM", 
        team_id: Optional[int] = None
    ) -> Note:
        """Create and persist a new note."""
        db_note = Note(
            owner_user_id=owner_user_id,
            text=text,
            visibility=visibility,
            team_id=team_id
        )
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return db_note

    def get(self, db: Session, note_id: int) -> Optional[Note]:
        """Retrieve a single note by its ID."""
        stmt = select(Note).where(Note.id == note_id)
        return db.scalars(stmt).first()

    def search(
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
        """Search and filter notes based on owner, team, visibility, or text content."""
        stmt = select(Note)

        if user_id is not None:
            stmt = stmt.where(Note.owner_user_id == user_id)
        
        if team_id is not None:
            stmt = stmt.where(Note.team_id == team_id)

        if visibility is not None:
            stmt = stmt.where(Note.visibility == visibility)

        if query_str:
            search_pattern = f"%{query_str}%"
            stmt = stmt.where(Note.text.ilike(search_pattern))

        stmt = stmt.offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    def update(
        self, 
        db: Session, 
        note_id: int, 
        *, 
        text: Optional[str] = None, 
        visibility: Optional[str] = None, 
        team_id: Optional[int] = None
    ) -> Optional[Note]:
        """Update an existing note's fields."""
        db_note = self.get(db, note_id)
        if not db_note:
            return None

        if text is not None:
            db_note.text = text
        if visibility is not None:
            db_note.visibility = visibility
        if team_id is not None:
            db_note.team_id = team_id

        db.commit()
        db.refresh(db_note)
        return db_note

    def delete(self, db: Session, note_id: int) -> bool:
        """Delete a note by its ID."""
        db_note = self.get(db, note_id)
        if not db_note:
            return False

        db.delete(db_note)
        db.commit()
        return True