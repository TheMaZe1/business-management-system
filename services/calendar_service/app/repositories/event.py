from app.models.event import CalendarEvent
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

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
