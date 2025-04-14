from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.calendar import CalendarRepository
from app.models.calendar import Calendar
from app.schemas.calendar import CalendarCreate
from app.database.db import get_db_session


class CalendarService:
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
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
    
    async def get_or_create_calendar(self, user_id: int) -> Calendar:
        calendar = await self.repo.get_by_user(user_id)
        if calendar:
            return calendar

        # Если календарь не найден — создаём новый
        new_calendar = Calendar(user_id=user_id)
        return await self.repo.create(new_calendar)

    async def get_calendar_with_events(self, user_id: int) -> Calendar:
        calendar = await self.repo.get_user_calendar_with_events(user_id)

        return calendar