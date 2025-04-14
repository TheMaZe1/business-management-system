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
    participant_ids: List[int]

    class Config:
        orm_mode = True
