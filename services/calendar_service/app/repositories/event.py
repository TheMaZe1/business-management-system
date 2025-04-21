from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from app.models.event import CalendarEvent


class CalendarEventRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, event: CalendarEvent):
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def list_by_calendar(self, calendar_id: int):
        result = await self.session.execute(
            select(CalendarEvent).where(CalendarEvent.calendar_id == calendar_id)
        )
        return result.scalars().all()

    async def update_partial(self, instance: CalendarEvent, data: dict) -> CalendarEvent:
    # Обновляем только те поля, которые были переданы
        for field, value in data.items():
            setattr(instance, field, value)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance
    
    async def delete(self, instance: CalendarEvent) -> bool:
        # Удаляем объект
        self.session.delete(instance)
        await self.session.commit()

        # Проверяем, что объект действительно был удалён (например, по количеству затронутых строк)
        deleted_count = await self.session.execute(
            select(func.count()).filter(CalendarEvent.id == instance.id)
        )
        if deleted_count.scalar() == 0:
            return True
        return False