from datetime import datetime

from pydantic import BaseModel


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes=True