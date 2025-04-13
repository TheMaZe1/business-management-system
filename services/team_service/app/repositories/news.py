# app/repositories/news.py

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.news import TeamNews

class SQLAlchemyNewsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, news: TeamNews) -> TeamNews:
        self.session.add(news)
        await self.session.commit()
        await self.session.refresh(news)
        return news

    async def list_by_team(self, team_id: int) -> list[TeamNews]:
        result = await self.session.execute(
            select(TeamNews).where(TeamNews.team_id == team_id).order_by(TeamNews.created_at.desc())
        )
        return result.scalars().all()

    async def get_by_id(self, team_id: int, news_id: int) -> Optional[TeamNews]:
        result = await self.session.execute(
            select(TeamNews).where(TeamNews.id == news_id, TeamNews.team_id == team_id)
        )
        return result.scalars().first()

    async def update(self, news: TeamNews) -> TeamNews:
        await self.session.commit()
        await self.session.refresh(news)
        return news