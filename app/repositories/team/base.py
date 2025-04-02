from abc import ABC, abstractmethod

from app.models.team import Team


class TeamsRepository(ABC):

    @abstractmethod
    def get_by_name(self, name: str) -> Team | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_invite_code(self, invite_code: str) -> Team | None:
        raise NotImplementedError

    @abstractmethod
    def add(self, model: Team) -> Team:
        raise NotImplementedError

    @abstractmethod
    def get(self, oid: str) -> Team | None:
        raise NotImplementedError

    @abstractmethod
    def update(self, oid: str, model: Team) -> Team:
        raise NotImplementedError

    @abstractmethod
    def list(self, start: int = 0, limit: int = 10) -> list[Team]:
        raise NotImplementedError