from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.event import CalendarEventRepository
from app.repositories.calendar import CalendarRepository
from app.models.event import CalendarEvent
from app.schemas.event import CalendarEventCreate, CalendarEventUpdate
from sqlalchemy.future import select
from datetime import datetime

from app.database.db import get_db_session

class CalendarEventService:
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.repo = CalendarEventRepository(db)
        self.calendar_repo = CalendarRepository(db)

    async def create_event(self, event_data: CalendarEventCreate) -> CalendarEvent:
        # Валидация календаря по ID
        calendar = await self.calendar_repo.get_by_id(event_data.calendar_id)
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
        event = await self.repo.get_by_id(event_id)
        if not event:
            raise ValueError("Event not found")

        # Проверка, что событие принадлежит календарю пользователя
        calendar = await self.calendar_repo.get_by_id(event.calendar_id)
        if not calendar or calendar.user_id != user_id:
            raise ValueError("You don't have permission to update this event")

        # Обновляем поля события
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(event, key, value)

        # Сохраняем обновленное событие
        return await self.repo.update(event)

    async def delete_event(self, event_id: int, user_id: int) -> None:
        # Получаем событие по ID
        event = await self.repo.get_by_id(event_id)
        if not event:
            raise ValueError("Event not found")

        # Проверка, что событие принадлежит календарю пользователя
        calendar = await self.calendar_repo.get_by_id(event.calendar_id)
        if not calendar or calendar.user_id != user_id:
            raise ValueError("You don't have permission to delete this event")

        # Удаляем событие
        await self.repo.delete(event)
