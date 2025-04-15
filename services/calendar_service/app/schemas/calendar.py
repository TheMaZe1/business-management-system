from datetime import datetime
from typing import List

from pydantic import BaseModel

class CalendarBase(BaseModel):
    is_team_calendar: bool = False

class CalendarCreate(CalendarBase):
    pass

class CalendarEventResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime
    is_meeting: bool
    task_id: int | None
    meeting_id: int | None

    class Config:
        from_attributes=True

class CalendarResponse(BaseModel):
    id: int
    user_id: int
    events: List[CalendarEventResponse] = []

    class Config:
        from_attributes=True
