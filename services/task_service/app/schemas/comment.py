from pydantic import BaseModel
from datetime import datetime


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True