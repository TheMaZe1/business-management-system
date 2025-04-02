from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.user.user import SQLAlchemyUsersRepository
from app.repositories.team.team import SQLAlchemyTeamsRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from fastapi import Depends
from app.database.db import get_db


class UserService:
    def __init__(self, db: Session = Depends(get_db)):
        self.user_repo = SQLAlchemyUsersRepository(db)
        self.team_repo = SQLAlchemyTeamsRepository(db)

    def add(self, user_data: UserCreate) -> UserResponse:
        existing_user = self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("User with this email already exists")

        team = self.team_repo.get_by_invite_code(user_data.invite_code)
        if not team:
            raise ValueError("Invalid invite code")
        
        user = User(
            last_name=user_data.last_name,
            name=user_data.name,
            email=user_data.email,
            password=user_data.password,
            team=team
        )

        return UserResponse.model_validate(self.user_repo.add(user))

    def update(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        # Проверяем, занят ли email
        if user_data.email:
            existing_user = self.user_repo.get_by_email(user_data.email)
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email is already in use")

        return UserResponse.model_validate(self.user_repo.update(user_id, user_data.model_dump(exclude_unset=True)))
    
    def get_by_email(self, email: str) -> UserResponse:
        existing_user = self.user_repo.get_by_email(email)
        if existing_user:
            return UserResponse.model_validate(existing_user)
        else:
            raise ValueError("User not found")
        
    def get_by_id(self, oid: str) -> UserResponse:
        existing_user = self.user_repo.get_by_id(oid)
        if existing_user:
            return UserResponse.model_validate(existing_user)
        else:
            raise ValueError("User not found")