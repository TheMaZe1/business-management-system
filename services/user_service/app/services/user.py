from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.jwt import Token
from app.database.db import get_db_session
from app.repositories.user import SQLAlchemyUsersRepository
from app.utils.jwt import create_access_token
from app.utils.password import hash_password, verify_password


class UserService:
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.user_repo = SQLAlchemyUsersRepository(db)

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        existing_user = await self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        user = User(
            last_name=user_data.last_name,
            name=user_data.name,
            email=user_data.email,
            password=hash_password(user_data.password)
        )

        saved_user = await self.user_repo.add(user)
        return UserResponse.model_validate(saved_user)

    async def update(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        if user_data.email and user_data.email != user.email:
            existing_user = await self.user_repo.get_by_email(user_data.email)
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email is already in use")

        updated_user = await self.user_repo.update(user_id, user_data.model_dump(exclude_unset=True))
        return UserResponse.model_validate(updated_user)
    
    async def get_by_email(self, email: str) -> UserResponse:
        existing_user = await self.user_repo.get_by_email(email)
        if existing_user:
            return UserResponse.model_validate(existing_user)
        else:
            raise ValueError("User not found")
        
    async def get_by_id(self, oid: int) -> UserResponse:
        existing_user = await self.user_repo.get_by_id(oid)
        if existing_user:
            return UserResponse.model_validate(existing_user)
        else:
            raise ValueError("User not found")
        
    async def soft_delete(self, user_id: int) -> UserResponse:
        user = await self.user_repo.soft_delete(user_id)
        if not user:
            raise ValueError("User not found")
        return UserResponse.model_validate(user)

    async def restore(self, user_id: int) -> UserResponse:
        user = await self.user_repo.restore(user_id)
        if not user:
            raise ValueError("User not found or restore window expired")
        return UserResponse.model_validate(user)

    async def authenticate_user(self, email: str, password: str) -> str:
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = create_access_token(
            data={"sub": str(user.id),
                  "email": user.email,
                  "name": user.name},
            expires_delta=timedelta(minutes=60)  # Экспирация токена
        )
        return access_token