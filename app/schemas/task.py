from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.task import TaskStatus
from app.schemas.user import UserResponse

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    assigned_to_id: int

class TaskResponse(TaskBase):
    id: int
    status: TaskStatus
    assigned_to: UserResponse
    created_by: UserResponse

    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None
