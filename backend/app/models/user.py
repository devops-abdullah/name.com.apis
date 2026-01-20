from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    team_id: int
    role: str  # admin, manager, member
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class UserInTeam(BaseModel):
    user_id: int
    team_id: int
    role: str
    joined_at: Optional[datetime] = None

    class Config:
        from_attributes = True
