from abc import ABC, abstractmethod

from app.models.user import User


class UsersRepository(ABC):

    @abstractmethod
    def get_by_fullname(self, surname: str, name: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def add(self, model: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def get(self, oid: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def update(self, oid: str, model: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def list(self, start: int = 0, limit: int = 10) -> list[User]:
        raise NotImplementedError