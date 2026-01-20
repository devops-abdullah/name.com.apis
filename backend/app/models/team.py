from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Team(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    owner_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TeamCreate(BaseModel):
    name: str
    description: Optional[str] = None

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class TeamMember(BaseModel):
    user_id: int
    username: str
    email: str
    role: str
    joined_at: datetime

class TeamDetail(Team):
    members: List[TeamMember] = []
    member_count: int = 0
