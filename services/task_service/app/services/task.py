# app/services/task.py

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.task import TaskRepository
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate
from app.database.db import get_db_session


class TaskService:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.repo = TaskRepository(session)


    async def create_task(self, team_id: int, department_id: int, task_data: TaskCreate, user_id: int):
        # Теперь принимаем и используем department_id, который также передается из URL
        new_task = Task(
            creator_id=user_id,
            title=task_data.title,
            description=task_data.description,
            assignee_id=task_data.assignee_id,
            team_id=team_id,  # team_id приходит из URL
            department_id=department_id,  # department_id тоже из URL
            due_date=task_data.due_date
        )
        await self.repo.add(new_task)
        return new_task


    async def get_task(self, task_id: int) -> Task:
        task = await self.repo.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        return task

    async def list_tasks_by_team(self, team_id: int, department_id: int) -> list[Task]:
        return await self.repo.list_by_team(team_id, department_id)

    async def update_task(self, task_id: int, data: TaskUpdate) -> Task:
        task = await self.get_task(task_id)
        for key, value in data.dict(exclude_unset=True).items():
            setattr(task, key, value)
        return await self.repo.update(task)

    async def delete_task(self, task_id: int):
        task = await self.get_task(task_id)
        await self.repo.delete(task)
