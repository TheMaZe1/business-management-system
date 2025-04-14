from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.meeting import Meeting
from app.models.event import CalendarEvent

class MeetingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, meeting: Meeting) -> Meeting:
        self.db.add(meeting)
        await self.db.flush()
        return meeting
    
    async def get_by_id(self, meeting_id: int) -> Meeting | None:
        result = await self.db.execute(
            select(Meeting).where(Meeting.id == meeting_id)
        )
        return result.scalars().first()

    async def get_by_team_id(self, team_id: int) -> list[Meeting]:
        result = await self.session.execute(
            select(Meeting).where(Meeting.team_id == team_id)
        )
        return result.scalars().all()
    
    async def get_by_id(self, meeting_id: int) -> Meeting | None:
        result = await self.session.execute(
            select(Meeting).where(Meeting.id == meeting_id)
        )
        return result.scalars().first()
    
    async def delete(self, meeting: Meeting):
        await self.session.delete(meeting)
        await self.session.commit()

    async def update(self, meeting: Meeting):
        self.session.add(meeting)
        await self.session.commit()
        await self.session.refresh(meeting)
        return meeting
    
    async def get_meeting_participants(self, meeting_id: int, team_id: int):
        events = await self.db.execute(
            select(CalendarEvent).where(
                CalendarEvent.meeting_id == meeting_id,
                CalendarEvent.team_id == team_id,
                CalendarEvent.is_meeting == True
            )
        )
        events = events.scalars().all()

        # Получаем id пользователей из календарей событий
        participant_ids = [event.calendar_id for event in events]

        return participant_ids  # Вернем ID участников