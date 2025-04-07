import datetime
from typing import Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user.base import UsersRepository


class SQLAlchemyUsersRepository(UsersRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_fullname(self, surname: str, name: str) -> Optional[User]:
        return self.session.query(User).filter(User.surname == surname, User.name == name).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).first()

    def add(self, model: User) -> User:
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def get_by_id(self, oid: str) -> Optional[User]:
        return self.session.query(User).filter(User.id == oid).first()

    def update(self, oid: str, user_data: dict) -> User:
        existing_user = self.get(oid)
        if not existing_user:
            return None

        for key, value in user_data.items():
            if value is not None:
                setattr(existing_user, key, value)

        self.session.commit()
        self.session.refresh(existing_user)
        return existing_user

    def soft_delete(self, oid: str) -> User:
        user = self.get_by_id(oid)
        if not user:
            return None
        user.is_deleted = True
        user.deleted_at = datetime.datetime.now()
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def restore(self, oid: str, restore_window_days: int = 7) -> User:
        user = self.get_by_id(oid)
        if not user or not user.is_deleted:
            return None

        if datetime.datetime.now() - user.deleted_at > datetime.timedelta(days=restore_window_days):
            return None  # истёк срок восстановления

        user.is_deleted = False
        user.deleted_at = None
        self.session.commit()
        self.session.refresh(user)
        return user


    def list(self, start: int = 0, limit: int = 10) -> list[User]:
        return self.session.query(User).offset(start).limit(limit).all()
