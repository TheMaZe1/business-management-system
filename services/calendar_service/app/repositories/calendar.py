from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from app.models.event import CalendarEvent
from app.models.calendar import Calendar

class CalendarRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, calendar: Calendar):
        self.session.add(calendar)
        await self.session.commit()
        await self.session.refresh(calendar)
        return calendar

    async def get_by_id(self, calendar_id: int):
        result = await self.session.execute(select(Calendar).where(Calendar.id == calendar_id))
        return result.scalar_one_or_none()
    
    async def get_by_user(self, user_id: int) -> Calendar | None:
        result = await self.session.execute(
            select(Calendar).where(Calendar.owner_id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def delete_by_meeting_id(self, meeting_id: int):
        await self.session.execute(
            delete(CalendarEvent).where(CalendarEvent.meeting_id == meeting_id)
        )
        await self.session.commit()

    async def get_user_calendar_with_events(self, user_id: int) -> Calendar | None:
        result = await self.session.execute(
            select(Calendar)
            .options(selectinload(Calendar.events))
            .where(
                Calendar.owner_id == user_id,
                Calendar.is_team_calendar == False
            )
        )
        return result.scalar_one_or_none()
