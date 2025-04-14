from fastapi import APIRouter, HTTPException, Depends, Request
from app.schemas.evaluation import TaskEvaluationCreate, TaskEvaluationResponse
from app.services.evaluation import TaskEvaluationService
from app.api.v1.routers.deps import get_current_user, get_membership
from app.services.task import TaskService
from app.schemas.membership import MembershipRole

router = APIRouter(
    prefix="/tasks/evaluations", 
    tags=["Task Evaluations"]
)

# Создание оценки
@router.post("/{task_id}", response_model=TaskEvaluationResponse)
async def create_task_evaluation(
    request: Request,
    task_id: int,
    evaluation_data: TaskEvaluationCreate,
    current_user: int = Depends(get_current_user),
    service: TaskEvaluationService = Depends(TaskEvaluationService),
    task_service: TaskService = Depends(TaskService)
):
    try:
        # Получаем задачу по ID
        task = await task_service.get_task_by_id(task_id)
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Проверяем, является ли current_user назначенным на задачу
        member = await get_membership(task.team_id, current_user, request)

        if member.role != MembershipRole.ADMIN and member.role != MembershipRole.MANAGER:
            raise HTTPException(status_code=403, detail="You must be an admin or manager to evaluate tasks")
        
        if task.assignee_id == current_user:
            raise HTTPException(status_code=403, detail="You cannot evaluate your own task")

        # Передаем данные для создания оценки
        evaluation = await service.create_task_evaluation(
            task_id=task_id,
            user_id=task.assignee_id,  # Оцененный пользователь (назначенный на задачу)
            evaluated_by_id=current_user,  # Оценивший (тот, кто оставляет оценку)
            evaluation_data=evaluation_data
        )
        return evaluation
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Получение всех оценок сотрудника
@router.get("/my-evaluations", response_model=list[TaskEvaluationResponse])
async def get_my_evaluations(current_user: int = Depends(get_current_user), service: TaskEvaluationService = Depends(TaskEvaluationService)):
    evaluations = await service.get_user_evaluations(user_id=current_user)
    return evaluations
