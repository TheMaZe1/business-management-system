from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.calendar import CalendarRepository
from app.models.calendar import Calendar
from app.schemas.calendar import CalendarCreate, CalendarResponse


class CalendarService:
    def __init__(self, db: AsyncSession):
        self.repo = CalendarRepository(db)

    async def create_calendar(self, owner_id: int, calendar_data: CalendarCreate) -> Calendar:
        calendar = Calendar(
            owner_id=owner_id,
            is_team_calendar=calendar_data.is_team_calendar
        )
        return await self.repo.create(calendar)
    
    async def get_by_user(self, user_id: int) -> Calendar:
        calendar = await self.repo.get_by_user(user_id)
        return calendar

    async def get_calendar_by_id(self, calendar_id: int) -> Calendar | None:
        return await self.repo.get_by_id(calendar_id)

    async def get_calendar_with_events(self, user_id: int) -> CalendarResponse:
        calendar = await self.repo.get_user_calendar_with_events(user_id)

        return CalendarResponse(
        id=calendar.id,
        user_id=calendar.owner_id,
        events=calendar.events
    )

    async def get_user_calendar_or_404(self, calendar_id: int, user_id: int) -> Calendar:
        calendar = await self.repo.get_by_id(calendar_id)
        if not calendar:
            raise HTTPException(status_code=404, detail="Calendar not found")
        if calendar.owner_id != user_id or calendar.is_team_calendar:
            raise HTTPException(status_code=403, detail="Access denied")
        return calendar