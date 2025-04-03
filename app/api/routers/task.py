from fastapi import APIRouter, Depends, HTTPException
from app.services.task import TaskService
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse)
def create_task(
    task_data: TaskCreate,
    created_by_id: int,
    service: TaskService = Depends(TaskService)
):
    try:
        return service.add(task_data, created_by_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate, service: TaskService = Depends(TaskService)):
    try:
        return service.update(task_id, task_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, service: TaskService = Depends(TaskService)):
    try:
        return service.get_by_id(task_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[TaskResponse])
def list_tasks(service: TaskService = Depends(TaskService), start: int = 0, limit: int = 10):
    return service.list(start, limit)

@router.delete("/{task_id}")
def delete_task(task_id: int, service: TaskService = Depends(TaskService)):
    try:
        service.delete(task_id)
        return {"message": "Task deleted"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
