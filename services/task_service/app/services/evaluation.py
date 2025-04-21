from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.evaluation import TaskEvaluationRepository
from app.schemas.evaluation import TaskEvaluationCreate, TaskEvaluationResponse
from app.models.evaluation import TaskEvaluation
from app.database.db import get_db_session

class TaskEvaluationService:
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.repo = TaskEvaluationRepository(db)

    async def create_task_evaluation(self, task_id: int, user_id: int, evaluated_by_id: int, evaluation_data: TaskEvaluationCreate) -> TaskEvaluationResponse:
        # Проверим, существует ли задача
        task = await self.repo.get_task_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        
        # Создаем новую оценку
        evaluation = TaskEvaluation(
            task_id=task_id,
            user_id=user_id,
            evaluated_by_id=evaluated_by_id,  # Оценивший пользователь
            deadline_score=evaluation_data.deadline_score,
            quality_score=evaluation_data.quality_score,
            completeness_score=evaluation_data.completeness_score
        )
        await self.repo.add(evaluation)
        return TaskEvaluationResponse.from_orm(evaluation)

    async def get_user_evaluations(self, user_id: int) -> list[TaskEvaluationResponse]:
        evaluations = await self.repo.get_evaluations_by_user(user_id)
        return [TaskEvaluationResponse.from_orm(evaluation) for evaluation in evaluations]

    async def get_quarterly_average_by_department(self, department_id: int, quarter: int) -> dict:
        evaluations = await self.repo.get_evaluations_by_department_and_quarter(department_id, quarter)
        total_score = 0
        count = 0
        for evaluation in evaluations:
            total_score += evaluation.average_score()
            count += 1
        return {"average_score": total_score / count if count else 0}
