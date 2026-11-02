from typing import Optional
from pydantic import BaseModel

class TeamBase(BaseModel):
    name: str

class TeamCreate(TeamBase):
    pass

class TeamUpdate(BaseModel):
    name: Optional[str] = None

class TeamResponse(TeamBase):
    id: int

    class Config:
        from_attributes = True