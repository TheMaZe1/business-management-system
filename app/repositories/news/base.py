from abc import ABC, abstractmethod
from app.models.news import News


class NewsRepository(ABC):

    @abstractmethod
    def add(self, news: News) -> News:
        pass

    @abstractmethod
    def list_by_team(self, team_id: int) -> list[News]:
        pass
