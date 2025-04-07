# schemas/evaluation.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EvaluationBase(BaseModel):
    score_timeliness: int
    score_quality: int
    score_completeness: int
    comment: Optional[str] = None

class EvaluationCreate(EvaluationBase):
    task_id: int

class EvaluationResponse(EvaluationBase):
    id: int
    evaluator_id: int
    created_at: datetime

    class Config:
        from_attributes = True

from pydantic import BaseModel

class AverageScoreResponse(BaseModel):
    user_id: int
    average_score: float  # Средний балл за период (например, за квартал)
    total_evaluations: int  # Количество оценок, по которым считается средний балл

    class Config:
        orm_mode = True
