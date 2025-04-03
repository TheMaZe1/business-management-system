from abc import ABC, abstractmethod
from app.models.meeting import Meeting

class MeetingRepository(ABC):

    @abstractmethod
    def get_by_id(self, meeting_id: int) -> Meeting | None:
        raise NotImplementedError

    @abstractmethod
    def list(self, start: int = 0, limit: int = 10) -> list[Meeting]:
        raise NotImplementedError

    @abstractmethod
    def add(self, meeting: Meeting) -> Meeting:
        raise NotImplementedError

    @abstractmethod
    def update(self, meeting_id: int, meeting_data: dict) -> Meeting:
        raise NotImplementedError

    @abstractmethod
    def delete(self, meeting_id: int) -> None:
        raise NotImplementedError
