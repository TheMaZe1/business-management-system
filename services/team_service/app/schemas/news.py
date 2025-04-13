# app/schemas/news.py

from datetime import datetime
from pydantic import BaseModel

class NewsCreate(BaseModel):
    title: str
    content: str

class NewsResponse(BaseModel):
    id: int
    team_id: int
    title: str
    content: str
    created_at: datetime

    class Config:
        from_attributes=True

# app/schemas/news.py

class NewsUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
