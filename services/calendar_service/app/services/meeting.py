from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.meeting import Meeting
from app.models.event import CalendarEvent
from app.repositories.meeting import MeetingRepository
from app.repositories.calendar import CalendarRepository
from app.repositories.event import CalendarEventRepository
from app.schemas.meeting import MeetingCreate, MeetingUpdate, MeetingResponse
from app.database.db import get_db_session

class MeetingService:
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.db = db
        self.repo = MeetingRepository(db)
        self.calendar_repo = CalendarRepository(db)
        self.event_repo = CalendarEventRepository(db)

    async def _build_response(self, meeting: Meeting) -> MeetingResponse:
        participant_ids = await self.repo.get_meeting_participants(meeting.id, meeting.team_id)
        return MeetingResponse.model_validate(meeting).model_copy(update={"participant_ids": participant_ids})

    async def create_meeting(self, organizer_id: int, team_id: int, data: MeetingCreate) -> MeetingResponse:
        if data.start_time >= data.end_time:
            raise ValueError("Invalid meeting time")

        meeting = Meeting(
            title=data.title,
            description=data.description,
            start_time=data.start_time,
            end_time=data.end_time,
            organizer_id=organizer_id,
            team_id=team_id
        )
        await self.repo.create(meeting)

        for user_id in data.participant_ids:
            calendar = await self.calendar_repo.get_by_user(user_id)
            event = CalendarEvent(
                calendar_id=calendar.id,
                title=data.title,
                description=data.description,
                start_time=data.start_time,
                end_time=data.end_time,
                is_meeting=True,
                meeting_id=meeting.id,
                team_id=team_id
            )
            await self.event_repo.create(event)

        return await self._build_response(meeting)

    async def get_meetings_by_team(self, team_id: int) -> list[MeetingResponse]:
        meetings = await self.repo.get_by_team_id(team_id)
        return [await self._build_response(m) for m in meetings]

    async def get_meeting_by_id(self, meeting_id: int) -> MeetingResponse | None:
        meeting = await self.repo.get_by_id(meeting_id)
        if not meeting:
            return None
        return await self._build_response(meeting)

    async def delete_meeting(self, meeting_id: int, current_user: int) -> bool:
        meeting = await self.repo.get_by_id(meeting_id)
        if not meeting or meeting.organizer_id != current_user:
            return False

        await self.event_repo.delete_by_meeting_id(meeting_id)
        await self.repo.delete(meeting)
        return True

    async def update_meeting(self, meeting_id: int, update_data: MeetingUpdate, current_user: int) -> MeetingResponse | None:
        meeting = await self.repo.get_by_id(meeting_id)
        if not meeting or meeting.organizer_id != current_user:
            return None

        if update_data.title:
            meeting.title = update_data.title
        if update_data.description is not None:
            meeting.description = update_data.description
        if update_data.start_time:
            meeting.start_time = update_data.start_time
        if update_data.end_time:
            meeting.end_time = update_data.end_time

        if update_data.participant_ids is not None:
            await self.event_repo.delete_by_meeting_id(meeting_id)
            for user_id in update_data.participant_ids:
                calendar = await self.calendar_repo.get_or_create_by_user(user_id)
                event = CalendarEvent(
                    calendar_id=calendar.id,
                    title=meeting.title,
                    description=meeting.description,
                    start_time=meeting.start_time,
                    end_time=meeting.end_time,
                    is_meeting=True,
                    meeting_id=meeting.id,
                    team_id=meeting.team_id
                )
                await self.event_repo.create(event)

        updated = await self.repo.update(meeting)
        return await self._build_response(updated)
