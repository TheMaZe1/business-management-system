from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.services.user import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.jwt import Token
from app.models.user import UserRole
from app.api.v1.routers.deps import get_current_user
from app.utils.broker import publish_user_created_event


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse)
async def register_user(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    service: UserService = Depends(UserService),
):
    try:
        user = await service.create_user(user_data)

    # Отложенная задача — публикация события
        background_tasks.add_task(publish_user_created_event, user.id)

        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    service: UserService = Depends(UserService),
    current_user: UserResponse = Depends(get_current_user)
):
    if current_user.id != user_id and current_user.role != UserRole.SUPERUSER:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    try:
        return await service.update(user_id, user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    service: UserService = Depends(UserService),
    current_user: UserResponse = Depends(get_current_user)
):
    if current_user.id != user_id and current_user.role != UserRole.SUPERUSER:
        raise HTTPException(status_code=403, detail="Not authorized to get this user")
    try:
        return await service.get_by_id(user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(
    user_id: int,
    service: UserService = Depends(UserService),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        return await service.get_by_id(current_user.user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}", response_model=UserResponse)
async def soft_delete_user(
    user_id: int,
    service: UserService = Depends(UserService),
    current_user: UserResponse = Depends(get_current_user)
):
    if current_user.id != user_id and current_user.role != UserRole.SUPERUSER:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    try:
        return await service.soft_delete(user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/restore/{user_id}", response_model=UserResponse)
async def restore_user(
    user_id: int,
    service: UserService = Depends(UserService),
    current_user: UserResponse = Depends(get_current_user)
):
    if current_user.id != user_id and current_user.role != UserRole.SUPERUSER:
        raise HTTPException(status_code=403, detail="Not authorized to restore this user")
    try:
        return await service.restore(user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
async def login_user(auth_data: OAuth2PasswordRequestForm = Depends(), service: UserService = Depends(UserService)):
    access_token = await service.authenticate_user(auth_data.username, auth_data.password)
    return Token.model_validate({"access_token": access_token, "token_type": "bearer"})