from sqlalchemy.orm import Session
from app.models.task import Task
from app.repositories.task.task import SQLAlchemyTaskRepository
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from fastapi import Depends
from app.database.db import get_db

class TaskService:
    def __init__(self, db: Session = Depends(get_db)):
        self.task_repo = SQLAlchemyTaskRepository(db)

    def add(self, task_data: TaskCreate, created_by_id: int) -> TaskResponse:
        task = Task(
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            assigned_to_id=task_data.assigned_to_id,
            created_by_id=created_by_id
        )
        return TaskResponse.model_validate(self.task_repo.add(task))

    def update(self, task_id: int, task_data: TaskUpdate) -> TaskResponse:
        existing_task = self.task_repo.get_by_id(task_id)
        if not existing_task:
            raise ValueError("Task not found")

        return TaskResponse.model_validate(
            self.task_repo.update(task_id, task_data.model_dump(exclude_unset=True))
        )

    def get_by_id(self, task_id: int) -> TaskResponse:
        task = self.task_repo.get_by_id(task_id)
        if task:
            return TaskResponse.model_validate(task)
        else:
            raise ValueError("Task not found")

    def list(self, start: int = 0, limit: int = 10) -> list[TaskResponse]:
        return [TaskResponse.model_validate(task) for task in self.task_repo.list(start, limit)]

    def delete(self, task_id: int) -> None:
        existing_task = self.task_repo.get_by_id(task_id)
        if not existing_task:
            raise ValueError("Task not found")
        self.task_repo.delete(task_id)
