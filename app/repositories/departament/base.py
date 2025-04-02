from abc import ABC, abstractmethod

from app.models.departament import Department


class DepartamentsRepository(ABC):

    @abstractmethod
    def get_by_name(self, name: str) -> Department | None:
        raise NotImplementedError

    @abstractmethod
    def add(self, model: Department) -> Department:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, oid: str) -> Department | None:
        raise NotImplementedError

    @abstractmethod
    def update(self, oid: str, user_data: dict) -> Department:
        raise NotImplementedError

    @abstractmethod
    def list(self, start: int = 0, limit: int = 10) -> list[Department]:
        raise NotImplementedError