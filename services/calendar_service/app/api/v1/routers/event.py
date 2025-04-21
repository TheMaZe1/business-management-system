from fastapi import APIRouter, Depends, HTTPException

from app.schemas.event import CalendarEventCreate, CalendarEventUpdate, CalendarEventResponse
from app.services.event import CalendarEventService
from app.api.v1.routers.deps import get_calendar_event_service, get_calendar_service, get_current_user
from app.services.calendar import CalendarService

router = APIRouter(
    prefix="/calendar", 
    tags=["Events"]
)

# Получить все события пользователя (по календарю)
@router.get("/events", response_model=list[CalendarEventResponse])
async def get_my_events(
    current_user: int = Depends(get_current_user),
    service_event: CalendarEventService = Depends(get_calendar_event_service),
    service_calendar: CalendarService = Depends(get_calendar_service)
):
    calendar = await service_calendar.get_user_calendar_or_404(current_user)
    events = await service_event.get_events_for_calendar(calendar.id)
    return events

# Создать событие
@router.post("/events", response_model=CalendarEventResponse)
async def create_event(
    event_data: CalendarEventCreate,
    current_user: int = Depends(get_current_user),
    service: CalendarEventService = Depends(get_calendar_event_service)
):
    try:
        event = await service.create_event(event_data=event_data, user_id=current_user)
        return event
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Получить событие по ID
@router.get("/events/{event_id}", response_model=CalendarEventResponse)
async def get_event(
    event_id: int,
    current_user: int = Depends(get_current_user),
    service: CalendarEventService = Depends(get_calendar_event_service)
):
    event = await service.ensure_event_access(event_id, current_user)
    
    return event

# Обновить событие
@router.put("/events/{event_id}", response_model=CalendarEventResponse)
async def update_event(
    event_id: int,
    update_data: CalendarEventUpdate,
    current_user: int = Depends(get_current_user),
    service: CalendarEventService = Depends(get_calendar_event_service)
):
    updated_event = await service.update_event(event_id, update_data, current_user)
    return updated_event

# Удалить событие
@router.delete("/events/{event_id}")
async def delete_event(
    event_id: int,
    current_user: int = Depends(get_current_user),
    service: CalendarEventService = Depends(get_calendar_event_service)
):
    success = await service.delete_event(event_id, current_user)
    if success:
        return {"detail": f"Event {event_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Event not found or access denied")
