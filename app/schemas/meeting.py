from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.user import UserResponse

class MeetingBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime

class MeetingCreate(MeetingBase):
    participants: List[int]

class MeetingResponse(MeetingBase):
    id: int
    created_by: UserResponse
    participants: List[UserResponse]

    class Config:
        from_attributes = True

class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    participants: Optional[List[int]] = None
