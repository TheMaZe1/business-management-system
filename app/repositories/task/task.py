from sqlalchemy.orm import Session
from app.models.task import Task
from app.repositories.task.base import TaskRepository

class SQLAlchemyTaskRepository(TaskRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, task_id: int) -> Task | None:
        return self.session.query(Task).filter(Task.id == task_id).first()

    def list(self, start: int = 0, limit: int = 10) -> list[Task]:
        return self.session.query(Task).offset(start).limit(limit).all()

    def add(self, task: Task) -> Task:
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def update(self, task_id: int, task_data: dict) -> Task:
        existing_task = self.get_by_id(task_id)
        if not existing_task:
            return None

        for key, value in task_data.items():
            if value is not None:
                setattr(existing_task, key, value)

        self.session.commit()
        self.session.refresh(existing_task)
        return existing_task

    def delete(self, task_id: int) -> None:
        task = self.get_by_id(task_id)
        if task:
            self.session.delete(task)
            self.session.commit()
