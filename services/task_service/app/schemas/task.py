from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.task import TaskStatus
from app.schemas.comment import CommentResponse


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    assignee_id: int
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    department_id: Optional[int] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None


class TaskResponse(TaskBase):
    id: int
    creator_id: int
    status: TaskStatus
    created_at: datetime

    class Config:
        orm_mode = True
