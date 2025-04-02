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

    def get(self, oid: str) -> Optional[User]:
        return self.session.query(User).filter(User.id == oid).first()

    def update(self, oid: str, model: User) -> User:
        existing_user = self.get(oid)
        if not existing_user:
            return None

        for key, value in model.__dict__.items():
            if value is not None:
                setattr(existing_user, key, value)

        self.session.commit()
        self.session.refresh(existing_user)
        return existing_user

    def list(self, start: int = 0, limit: int = 10) -> list[User]:
        return self.session.query(User).offset(start).limit(limit).all()
