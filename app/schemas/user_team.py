from pydantic import BaseModel

class UserTeamCreate(BaseModel):
    user_id: int
    team_id: int
    role: str = "MEMBER"

class UserTeamUpdate(BaseModel):
    role: str

class UserTeamResponse(BaseModel):
    user_id: int
    team_id: int
    role: str

    class Config:
        from_attributes = True