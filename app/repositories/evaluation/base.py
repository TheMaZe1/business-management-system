# repositories/evaluation/base.py

from abc import ABC, abstractmethod
from app.models.evaluation import Evaluation


class EvaluationRepository(ABC):
    @abstractmethod
    def add(self, evaluation: Evaluation) -> Evaluation:
        raise NotImplementedError

    @abstractmethod
    def get_by_task(self, task_id: int) -> Evaluation | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_user(self, user_id: int) -> list[Evaluation]:
        raise NotImplementedError
