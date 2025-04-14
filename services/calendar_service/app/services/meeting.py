from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.meeting import Meeting
from app.models.event import CalendarEvent
from app.repositories.meeting import MeetingRepository
from app.repositories.calendar import CalendarRepository
from app.repositories.event import CalendarEventRepository
from app.schemas.meeting import MeetingCreate
from app.database.db import get_db_session

class MeetingService:
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.db = db
        self.repo = MeetingRepository(db)
        self.calendar_repo = CalendarRepository(db)
        self.event_repo = CalendarEventRepository(db)

async def create_meeting(self, organizer_id: int, data: MeetingCreate) -> Meeting:
        if data.start_time >= data.end_time:
            raise ValueError("Invalid meeting time")

        # Создаём саму встречу
        meeting = Meeting(
            title=data.title,
            description=data.description,
            start_time=data.start_time,
            end_time=data.end_time,
            organizer_id=organizer_id,
            participant_ids=data.participant_ids  # это JSON поле или Array, зависит от модели
        )
        await self.repo.create(meeting)

        # Добавляем событие в календари участников
        for user_id in data.participant_ids:
            calendar = await self.calendar_repo.get_or_create_by_user(user_id)
            event = CalendarEvent(
                calendar_id=calendar.id,
                title=data.title,
                description=data.description,
                start_time=data.start_time,
                end_time=data.end_time,
                is_meeting=True,
                meeting_id=meeting.id
            )
            await self.event_repo.create(event)

        return meeting
