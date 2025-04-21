from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class MeetingBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime

class MeetingCreate(MeetingBase):
    participant_ids: List[int]

class MeetingResponse(MeetingBase):
    id: int
    organizer_id: int
    participant_ids: List[int] = []

    class Config:
        from_attributes=True

class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    participant_ids: Optional[List[int]] = None  # Список ID участников для обновления

    class Config:
        from_attributes=True
