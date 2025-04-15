from enum import Enum

from sqlalchemy import Column, Integer, String, Text, Enum as SQLEnum, DateTime, func
from sqlalchemy.orm import relationship

from app.database.db import Base

class TaskStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.OPEN)
    assignee_id = Column(Integer, nullable=False)
    creator_id = Column(Integer, nullable=False)
    team_id = Column(Integer, nullable=False)
    department_id = Column(Integer, nullable=True)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())

    comments = relationship("Comment", back_populates="task")
    evaluations = relationship("TaskEvaluation", back_populates="task")



