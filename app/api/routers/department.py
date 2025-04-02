from fastapi import APIRouter, Depends, HTTPException
from app.schemas.departament import DepartmentCreate, DepartmentResponse, DepartmentUpdate
from app.services.departament import DepartamentService
from app.services.user import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.post("/", response_model=DepartmentResponse)
def register_department(department_data: DepartmentCreate = Depends, service: DepartamentService = Depends(DepartamentService)):
    try:
        return service.add(department_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{department_id}", response_model=DepartmentResponse)
def update_user(department_id: int, department_data: DepartmentUpdate, service: DepartamentService = Depends(DepartamentService)):
    try:
        return service.update(department_id, department_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{department_id}", response_model=DepartmentResponse)
def get_user(department_id: int, service: DepartamentService = Depends(DepartamentService)):
    try:
        return service.get_by_id(department_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
