from fastapi import APIRouter, Depends, HTTPException
from app.schemas.event import CalendarEventCreate, CalendarEventUpdate, CalendarEventResponse
from app.services.event import CalendarEventService
from app.api.v1.routers.deps import get_current_user

router = APIRouter(
    prefix="/calendar", 
    tags=["Events"]
)

# Получить все события пользователя (по календарю)
@router.get("/events", response_model=list[CalendarEventResponse])
async def get_my_events(
    current_user: int = Depends(get_current_user),
    service: CalendarEventService = Depends(CalendarEventService)
):
    # Здесь будем использовать информацию о текущем пользователе для получения календаря (через get_by_user)
    # или передавать ID календаря, если он связан с пользователем
    try:
        calendar = await service.calendar_repo.get_by_user(current_user)
        if not calendar:
            raise HTTPException(status_code=404, detail="Calendar not found")

        events = await service.get_events_for_calendar(calendar.id)
        return events
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Создать событие
@router.post("/events", response_model=CalendarEventResponse)
async def create_event(
    event_data: CalendarEventCreate,
    current_user: int = Depends(get_current_user),
    service: CalendarEventService = Depends(CalendarEventService)
):
    try:
        # Здесь календарь будет уже проверяться в сервисе для пользователя, который делает запрос
        event = await service.create_event(event_data=event_data)
        return event
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Получить событие по ID
@router.get("/events/{event_id}", response_model=CalendarEventResponse)
async def get_event(
    event_id: int,
    current_user: int = Depends(get_current_user),
    service: CalendarEventService = Depends(CalendarEventService)
):
    try:
        event = await service.repo.get_by_id(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Дополнительная проверка: доступность события для текущего пользователя
        calendar = await service.calendar_repo.get_by_id(event.calendar_id)
        if calendar.user_id != current_user:
            raise HTTPException(status_code=403, detail="You do not have access to this event")

        return event
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Обновить событие
@router.put("/events/{event_id}", response_model=CalendarEventResponse)
async def update_event(
    event_id: int,
    update_data: CalendarEventUpdate,
    current_user: int = Depends(get_current_user),
    service: CalendarEventService = Depends(CalendarEventService)
):
    try:
        event = await service.repo.get_by_id(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        # Проверим, что пользователь имеет доступ к этому событию
        calendar = await service.calendar_repo.get_by_id(event.calendar_id)
        if calendar.user_id != current_user:
            raise HTTPException(status_code=403, detail="You do not have access to this event")

        # Выполним обновление
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(event, key, value)

        updated_event = await service.repo.update(event)
        return updated_event
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Удалить событие
@router.delete("/events/{event_id}")
async def delete_event(
    event_id: int,
    current_user: int = Depends(get_current_user),
    service: CalendarEventService = Depends(CalendarEventService)
):
    try:
        event = await service.repo.get_by_id(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        # Проверим, что пользователь имеет доступ к этому событию
        calendar = await service.calendar_repo.get_by_id(event.calendar_id)
        if calendar.user_id != current_user:
            raise HTTPException(status_code=403, detail="You do not have access to this event")

        await service.repo.delete(event)
        return {"detail": "Event deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
