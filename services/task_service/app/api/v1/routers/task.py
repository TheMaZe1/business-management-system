from fastapi import APIRouter, Depends, HTTPException, Request, status
from app.services.task import TaskService
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.api.v1.routers.deps import get_current_user, get_membership
from app.schemas.membership import MembershipRole

router = APIRouter(
    prefix="/teams/{team_id}/{department_id}/tasks",
    tags=["Tasks"],
)


@router.post("/", response_model=TaskResponse)
async def create_task(
    request: Request,
    team_id: int,
    department_id: int,
    task_in: TaskCreate,
    current_user: int = Depends(get_current_user),
    service: TaskService = Depends(TaskService),
):
    member = await get_membership(team_id, current_user, request)
    if member.role not in [MembershipRole.ADMIN, MembershipRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Only admins or managers can create tasks")

    task = await service.create_task(team_id=team_id, department_id=department_id, task_data=task_in, user_id=current_user)
    return task


@router.get("/", response_model=list[TaskResponse])
async def list_tasks(
    request: Request,
    team_id: int,
    department_id: int,
    current_user: int = Depends(get_current_user),
    service: TaskService = Depends(TaskService),
):
    await get_membership(team_id, current_user, request)
    return await service.list_tasks_by_team(team_id, department_id)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    request: Request,
    team_id: int,
    task_id: int,
    department_id: int,
    current_user: int = Depends(get_current_user),
    service: TaskService = Depends(TaskService),
):
    await get_membership(team_id, current_user, request)
    task = await service.get_task(task_id)
    if task.team_id != team_id:
        raise HTTPException(status_code=404, detail="Task not found in this team")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    request: Request,
    team_id: int,
    task_id: int,
    department_id: int,
    task_update: TaskUpdate,
    current_user: int = Depends(get_current_user),
    service: TaskService = Depends(TaskService),
):
    member = await get_membership(team_id, current_user, request)
    if member.role not in [MembershipRole.ADMIN, MembershipRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Only admins or managers can update tasks")

    task = await service.get_task(task_id)
    if task.team_id != team_id:
        raise HTTPException(status_code=404, detail="Task not found in this team")

    return await service.update_task(task_id, task_update)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    request: Request,
    team_id: int,
    task_id: int,
    department_id: int,
    current_user: int = Depends(get_current_user),
    service: TaskService = Depends(TaskService),
):
    member = await get_membership(team_id, current_user, request)
    if member.role not in [MembershipRole.ADMIN, MembershipRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Only admins or managers can delete tasks")

    task = await service.get_task(task_id)
    if task.team_id != team_id:
        raise HTTPException(status_code=404, detail="Task not found in this team")

    await service.delete_task(task_id)
