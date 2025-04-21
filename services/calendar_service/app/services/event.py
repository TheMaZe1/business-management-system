import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.event import CalendarEventRepository
from app.repositories.calendar import CalendarRepository
from app.models.event import CalendarEvent
from app.schemas.event import CalendarEventCreate, CalendarEventUpdate

logger = logging.getLogger(__name__)

class CalendarEventService:
    def __init__(self, db: AsyncSession):
        self.repo = CalendarEventRepository(db)
        self.calendar_repo = CalendarRepository(db)

    async def create_event(self, event_data: CalendarEventCreate, user_id: int) -> CalendarEvent:
        # Валидация календаря по ID
        calendar = await self.calendar_repo.get_by_user(user_id)
        if not calendar:
            raise ValueError("Calendar not found")

        # Валидация времени (начало должно быть раньше конца)
        if event_data.start_time >= event_data.end_time:
            raise ValueError("Invalid time range")

        # Создание нового события
        event = CalendarEvent(
            calendar_id=event_data.calendar_id,
            title=event_data.title,
            description=event_data.description,
            start_time=event_data.start_time,
            end_time=event_data.end_time,
            is_meeting=event_data.is_meeting,
            task_id=event_data.task_id
        )

        # Сохраняем событие в базе данных
        return await self.repo.create(event)

    async def get_events_for_calendar(self, calendar_id: int) -> list[CalendarEvent]:
        # Получение всех событий для календаря
        return await self.repo.list_by_calendar(calendar_id)

    async def get_event(self, event_id: int, user_id: int) -> CalendarEvent:
        # Получение события по ID
        event = await self.repo.get_by_id(event_id)
        if not event:
            return None

        # Проверка, что событие принадлежит календарю пользователя
        calendar = await self.calendar_repo.get_by_id(event.calendar_id)
        if calendar and calendar.user_id == user_id:
            return event
        return None

    async def update_event(self, event_id: int, user_id: int, update_data: CalendarEventUpdate) -> CalendarEvent:
        # Получаем событие по ID
        event = await self.ensure_event_access(event_id, user_id)
        
        # Переводим данные в словарь и передаем в репозиторий
        update_dict = update_data.dict(exclude_unset=True)
        
        # Используем update_partial для обновления
        updated_event = await self.repo.update_partial(event, update_dict)
        
        return updated_event

    async def delete_event(self, event_id: int, current_user: int) -> bool:
        event = await self.ensure_event_access(event_id, current_user)

        # Удаляем событие
        success = await self.repo.delete(event)
        
        if success:
            # Можно добавить логирование о успешном удалении
            logger.info(f"Event {event_id} deleted successfully by user {current_user}")
            return True
        else:
            # Можно добавить логирование о неудачном удалении
            logger.error(f"Failed to delete event {event_id} by user {current_user}")
            return False

    async def ensure_event_access(self, event_id: int, current_user: int):
        event = await self.event_repo.get_by_id(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        calendar = await self.calendar_repo.get_by_id(event.calendar_id)
        if not calendar or calendar.owner_id != current_user:
            raise HTTPException(status_code=403, detail="Access denied to this event")
        
        return event