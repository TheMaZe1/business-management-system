from fastapi import APIRouter, Depends, HTTPException
from app.schemas.news import NewsCreate, NewsResponse
from app.services.news import NewsService

router = APIRouter(prefix="/news", tags=["News"])

@router.post("/", response_model=NewsResponse)
def publish_news(news_data: NewsCreate, service: NewsService = Depends()):
    try:
        return service.create(news_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/team/{team_id}", response_model=list[NewsResponse])
def get_team_news(team_id: int, service: NewsService = Depends()):
    return service.get_team_news(team_id)
