from fastapi import APIRouter, Depends, HTTPException
from app.services.calendar import CalendarService
from app.schemas.calendar import CalendarResponse
from app.api.v1.routers.deps import get_current_user
from app.schemas.calendar import CalendarCreate, CalendarResponse

router = APIRouter(prefix="/calendar", tags=["Calendar"])


@router.post("", response_model=CalendarResponse)
async def create_calendar(
    calendar_data: CalendarCreate,
    current_user: int = Depends(get_current_user),
    service: CalendarService = Depends(CalendarService)
):
    calendar = await service.create_calendar(owner_id=current_user, calendar_data=calendar_data)
    return calendar

# Получить календарь пользователя
@router.get("", response_model=CalendarResponse)
async def get_calendar(
    current_user: int = Depends(get_current_user),
    service: CalendarService = Depends(CalendarService)
):
    calendar = await service.get_or_create_calendar(current_user)
    return calendar

# Удалить календарь (опционально)
@router.delete("")
async def delete_calendar(
    current_user: int = Depends(get_current_user),
    service: CalendarService = Depends(CalendarService)
):
    await service.delete_calendar(current_user)
    return {"detail": "Calendar deleted"}