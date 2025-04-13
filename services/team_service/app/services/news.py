# app/services/news.py

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.news import SQLAlchemyNewsRepository
from app.schemas.news import NewsCreate, NewsResponse
from app.models.news import TeamNews
from app.database.db import get_db_session

from app.schemas.news import NewsUpdate
from sqlalchemy import select

class NewsService:
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.repo = SQLAlchemyNewsRepository(db)

    async def create(self, team_id: int, data: NewsCreate) -> NewsResponse:
        news = TeamNews(team_id=team_id, title=data.title, content=data.content)
        saved = await self.repo.add(news)
        return NewsResponse.from_orm(saved)

    async def get_by_team(self, team_id: int) -> list[NewsResponse]:
        items = await self.repo.list_by_team(team_id)
        return [NewsResponse.from_orm(item) for item in items]

    async def get_by_id(self, team_id: int, news_id: int) -> NewsResponse:
        news = await self.repo.get_by_id(team_id, news_id)
        if not news:
            raise ValueError("News not found")
        return NewsResponse.from_orm(news)

    async def update(self, team_id: int, news_id: int, data: NewsUpdate) -> NewsResponse:
        news = await self.repo.get_by_id(team_id, news_id)
        if not news:
            raise ValueError("News not found")

        if data.title is not None:
            news.title = data.title
        if data.content is not None:
            news.content = data.content

        updated_news = await self.repo.update(news)
        return NewsResponse.from_orm(updated_news)