from fastapi import APIRouter, Depends, HTTPException
from app.services.user import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def register_user(user_data: UserCreate = Depends, service: UserService = Depends(UserService)):
    try:
        return service.add(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, service: UserService = Depends(UserService)):
    try:
        return service.update(user_id, user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, service: UserService = Depends(UserService)):
    try:
        return service.get_by_id(user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.delete("/{user_id}")
def soft_delete_user(user_id: int, service: UserService = Depends(UserService)):
    try:
        return service.soft_delete(user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/restore/{user_id}")
def restore_user(user_id: int, service: UserService = Depends(UserService)):
    try:
        return service.restore(user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

