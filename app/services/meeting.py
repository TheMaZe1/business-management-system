from sqlalchemy.orm import Session
from app.models.meeting import Meeting
from app.models.user import User
from app.repositories.meeting.meeting import SQLAlchemyMeetingRepository
from app.repositories.user.user import SQLAlchemyUsersRepository
from app.schemas.meeting import MeetingCreate, MeetingUpdate, MeetingResponse
from fastapi import Depends
from app.database.db import get_db

class MeetingService:
    def __init__(self, db: Session = Depends(get_db)):
        self.meeting_repo = SQLAlchemyMeetingRepository(db)
        self.user_repo = SQLAlchemyUsersRepository(db)

    def add(self, meeting_data: MeetingCreate, created_by_id: int) -> MeetingResponse:

        participants = [self.user_repo.get_by_id(user_id) for user_id in meeting_data.participants]

        meeting = Meeting(
            title=meeting_data.title,
            description=meeting_data.description,
            start_time=meeting_data.start_time,
            end_time=meeting_data.end_time,
            created_by_id=created_by_id,
            participants=participants  # Преобразуем ID в объекты User
        )
        return MeetingResponse.model_validate(self.meeting_repo.add(meeting))

    def update(self, meeting_id: int, meeting_data: MeetingUpdate) -> MeetingResponse:
        existing_meeting = self.meeting_repo.get_by_id(meeting_id)
        if not existing_meeting:
            raise ValueError("Meeting not found")

        return MeetingResponse.model_validate(
            self.meeting_repo.update(meeting_id, meeting_data.model_dump(exclude_unset=True))
        )

    def get_by_id(self, meeting_id: int) -> MeetingResponse:
        meeting = self.meeting_repo.get_by_id(meeting_id)
        if meeting:
            return MeetingResponse.model_validate(meeting)
        else:
            raise ValueError("Meeting not found")

    def list(self, start: int = 0, limit: int = 10) -> list[MeetingResponse]:
        return [MeetingResponse.model_validate(meeting) for meeting in self.meeting_repo.list(start, limit)]

    def delete(self, meeting_id: int) -> None:
        existing_meeting = self.meeting_repo.get_by_id(meeting_id)
        if not existing_meeting:
            raise ValueError("Meeting not found")
        self.meeting_repo.delete(meeting_id)
