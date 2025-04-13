# app/api/v1/routers/news.py

from fastapi import APIRouter, Depends, HTTPException
from app.services.news import NewsService
from app.services.membership import MembershipService
from app.schemas.news import NewsCreate, NewsResponse, NewsUpdate
from app.api.v1.routers.deps import get_current_user, get_membership
from app.models.membership import MembershipRole

router = APIRouter(prefix="/teams/{team_id}/news", tags=["Team News"])

@router.post("/", response_model=NewsResponse)
async def create_news(
    team_id: int,
    data: NewsCreate,
    current_user: int = Depends(get_current_user),
    news_service: NewsService = Depends(NewsService),
    membership_service: MembershipService = Depends(MembershipService),
):
    member = await get_membership(team_id, current_user, membership_service)
    if member.role != MembershipRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can create news")
    return await news_service.create(team_id, data)


@router.get("/", response_model=list[NewsResponse])
async def list_news(
    team_id: int,
    current_user: int = Depends(get_current_user),
    news_service: NewsService = Depends(NewsService),
    membership_service: MembershipService = Depends(MembershipService),
):
    await get_membership(team_id, current_user, membership_service)  # только для участников
    return await news_service.get_by_team(team_id)


@router.get("/{news_id}", response_model=NewsResponse)
async def get_news_item(
    team_id: int,
    news_id: int,
    current_user: int = Depends(get_current_user),
    news_service: NewsService = Depends(NewsService),
    membership_service: MembershipService = Depends(MembershipService),
):
    await get_membership(team_id, current_user, membership_service)
    try:
        return await news_service.get_by_id(team_id, news_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{news_id}", response_model=NewsResponse)
async def update_news_item(
    team_id: int,
    news_id: int,
    data: NewsUpdate,
    current_user: int = Depends(get_current_user),
    news_service: NewsService = Depends(NewsService),
    membership_service: MembershipService = Depends(MembershipService),
):
    member = await get_membership(team_id, current_user, membership_service)
    if member.role != MembershipRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can update news")
    
    try:
        return await news_service.update(team_id, news_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))