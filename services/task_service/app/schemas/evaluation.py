from datetime import datetime

from pydantic import BaseModel

class TaskEvaluationCreate(BaseModel):
    deadline_score: float
    quality_score: float
    completeness_score: float

class TaskEvaluationResponse(BaseModel):
    task_id: int
    user_id: int
    evaluated_by_id: int
    deadline_score: float
    quality_score: float
    completeness_score: float
    evaluation_date: datetime

    class Config:
        from_attributes=True
