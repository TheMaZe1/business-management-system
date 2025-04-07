from sqlalchemy.orm import Session
from fastapi import Depends
from app.database.db import get_db
from app.schemas.news import NewsCreate, NewsResponse
from app.models.news import News
from app.repositories.news.news import SQLAlchemyNewsRepository


class NewsService:
    def __init__(self, db: Session = Depends(get_db)):
        self.repo = SQLAlchemyNewsRepository(db)

    def create(self, news_data: NewsCreate) -> NewsResponse:
        news = News(**news_data.model_dump())
        return NewsResponse.model_validate(self.repo.add(news))

    def get_team_news(self, team_id: int) -> list[NewsResponse]:
        news_list = self.repo.list_by_team(team_id)
        return [NewsResponse.model_validate(n) for n in news_list]
