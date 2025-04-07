# repositories/evaluation/evaluation.py

from sqlalchemy.orm import Session
from typing import Optional

from app.models.evaluation import Evaluation
from app.models.task import Task
from app.repositories.evaluation.base import EvaluationRepository


class SQLAlchemyEvaluationRepository(EvaluationRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, evaluation: Evaluation) -> Evaluation:
        self.session.add(evaluation)
        self.session.commit()
        self.session.refresh(evaluation)
        return evaluation

    def get_by_task(self, task_id: int) -> Optional[Evaluation]:
        return self.session.query(Evaluation).filter(Evaluation.task_id == task_id).first()

    def get_by_user(self, user_id: int) -> list[Evaluation]:
        return (
            self.session.query(Evaluation)
            .join(Task)
            .filter(Task.assignee_id == user_id)
            .all()
        )
