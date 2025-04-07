from pydantic import BaseModel
from datetime import datetime


class NewsCreate(BaseModel):
    title: str
    content: str
    team_id: int


class NewsResponse(NewsCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
