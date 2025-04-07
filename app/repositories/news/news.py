from sqlalchemy.orm import Session
from app.models.news import News
from app.repositories.news.base import NewsRepository


class SQLAlchemyNewsRepository(NewsRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, news: News) -> News:
        self.session.add(news)
        self.session.commit()
        self.session.refresh(news)
        return news

    def list_by_team(self, team_id: int) -> list[News]:
        return self.session.query(News).filter(News.team_id == team_id).order_by(News.created_at.desc()).all()
