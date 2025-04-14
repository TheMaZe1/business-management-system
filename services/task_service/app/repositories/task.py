# app/repositories/task.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.task import Task
from app.models.comment import Comment
from typing import List

class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, task: Task) -> Task:
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_by_id(self, task_id: int) -> Task | None:
        result = await self.session.execute(select(Task).filter(Task.id == task_id))
        return result.scalars().first()

    async def list_by_team(self, team_id: int, department_id: id) -> List[Task]:
        result = await self.session.execute(select(Task).filter(Task.team_id == team_id, Task.department_id == department_id))
        return result.scalars().all()

    async def delete(self, task: Task):
        await self.session.delete(task)
        await self.session.commit()

    async def update(self, task: Task) -> Task:
        await self.session.commit()
        await self.session.refresh(task)
        return task
