from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.evaluation import TaskEvaluation
from app.models.task import Task


class TaskEvaluationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Метод для добавления оценки
    async def add(self, evaluation: TaskEvaluation):
        self.db.add(evaluation)
        await self.db.commit()
        await self.db.refresh(evaluation)
        return evaluation

    # Метод для получения всех оценок по задаче
    async def get_by_task_by_id(self, task_id: int) -> list[TaskEvaluation]:
        result = await self.db.execute(
            select(TaskEvaluation).where(TaskEvaluation.task_id == task_id)
        )
        return result.scalars().all()

    # Метод для получения всех оценок сотрудника
    async def get_evaluations_by_user(self, user_id: int) -> list[TaskEvaluation]:
        result = await self.db.execute(
            select(TaskEvaluation).where(TaskEvaluation.user_id == user_id)
        )
        return result.scalars().all()

    # Метод для получения всех оценок по подразделению и кварталу
    async def get_evaluations_by_department_and_quarter(self, department_id: int, quarter: int) -> list[TaskEvaluation]:
        result = await self.db.execute(
            select(TaskEvaluation)
            .join(Task)
            .where(Task.department_id == department_id)
        )
        return result.scalars().all()

    # Получение задачи по ID
    async def get_task_by_id(self, task_id: int) -> Task | None:
        result = await self.db.execute(
            select(Task).where(Task.id == task_id)
        )
        return result.scalar_one_or_none()
    
