from pydantic import BaseModel, EmailStr
from typing import Optional

from app.models.user import UserRole
from app.schemas.team import TeamResponse

class UserBase(BaseModel):
    last_name: str
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    invite_code: str 

class UserResponse(UserBase):
    id: int
    team: TeamResponse
    role: UserRole

    class Config:
        from_attributes = True
    
class UserUpdate(BaseModel):
    last_name: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
