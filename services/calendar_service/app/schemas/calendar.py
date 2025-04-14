from pydantic import BaseModel
from typing import Optional

class CalendarBase(BaseModel):
    name: str
    is_team_calendar: bool = False

class CalendarCreate(CalendarBase):
    pass

class CalendarResponse(CalendarBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
