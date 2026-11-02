from typing import Optional
from pydantic import BaseModel

class NoteCreate(BaseModel):
    text: str
    visibility: str = "TEAM"
    team_id: Optional[int] = None

class NoteUpdate(BaseModel):
    text: Optional[str] = None
    visibility: Optional[str] = None
    team_id: Optional[int] = None

class NoteResponse(BaseModel):
    id: int
    owner_user_id: int
    text: str
    visibility: str
    team_id: Optional[int] = None

    class Config:
        from_attributes = True