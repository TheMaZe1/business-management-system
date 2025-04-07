from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.evaluation import Evaluation
from app.repositories.evaluation.evaluation import SQLAlchemyEvaluationRepository
from app.repositories.task.task import SQLAlchemyTaskRepository
from app.schemas.evaluation import EvaluationCreate, EvaluationResponse


class EvaluationService:
    def __init__(self, db: Session = Depends(get_db)):
        self.repo = SQLAlchemyEvaluationRepository(db)
        self.task_repo = SQLAlchemyTaskRepository(db)  # уже должен быть

    def evaluate(self, evaluator_id: int, data: EvaluationCreate) -> EvaluationResponse:
        task = self.task_repo.get_by_id(data.task_id)
        if not task:
            raise ValueError("Task not found")

        if task.evaluation:
            raise ValueError("Task already evaluated")

        # Допустим, у задачи есть поле manager_id
        if task.manager_id != evaluator_id:
            raise ValueError("Only the manager can evaluate this task")

        evaluation = Evaluation(
            task_id=data.task_id,
            evaluator_id=evaluator_id,
            score_timeliness=data.score_timeliness,
            score_quality=data.score_quality,
            score_completeness=data.score_completeness,
            comment=data.comment,
        )
        return EvaluationResponse.model_validate(self.repo.add(evaluation))

    def get_user_scores(self, user_id: int) -> list[EvaluationResponse]:
        evaluations = self.repo.get_by_user(user_id)
        return [EvaluationResponse.model_validate(ev) for ev in evaluations]
