from abc import ABC, abstractmethod
from app.models.task import Task

class TaskRepository(ABC):

    @abstractmethod
    def get_by_id(self, task_id: int) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    def list(self, start: int = 0, limit: int = 10) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    def add(self, task: Task) -> Task:
        raise NotImplementedError

    @abstractmethod
    def update(self, task_id: int, task_data: dict) -> Task:
        raise NotImplementedError

    @abstractmethod
    def delete(self, task_id: int) -> None:
        raise NotImplementedError
