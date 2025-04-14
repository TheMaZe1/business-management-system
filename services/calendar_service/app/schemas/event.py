from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CalendarEventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    is_meeting: bool = False
    task_id: Optional[int] = None

class CalendarEventCreate(CalendarEventBase):
    calendar_id: int

class CalendarEventResponse(CalendarEventBase):
    id: int
    calendar_id: int

    class Config:
        orm_mode = True

class CalendarEventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_meeting: Optional[bool] = None
    task_id: Optional[int] = None