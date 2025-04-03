from sqlalchemy.orm import Session
from app.models.meeting import Meeting
from app.repositories.meeting.base import MeetingRepository

class SQLAlchemyMeetingRepository(MeetingRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, meeting_id: int) -> Meeting | None:
        return self.session.query(Meeting).filter(Meeting.id == meeting_id).first()

    def list(self, start: int = 0, limit: int = 10) -> list[Meeting]:
        return self.session.query(Meeting).offset(start).limit(limit).all()

    def add(self, meeting: Meeting) -> Meeting:
        self.session.add(meeting)
        self.session.commit()
        self.session.refresh(meeting)
        return meeting

    def update(self, meeting_id: int, meeting_data: dict) -> Meeting:
        existing_meeting = self.get_by_id(meeting_id)
        if not existing_meeting:
            return None

        for key, value in meeting_data.items():
            if value is not None:
                setattr(existing_meeting, key, value)

        self.session.commit()
        self.session.refresh(existing_meeting)
        return existing_meeting

    def delete(self, meeting_id: int) -> None:
        meeting = self.get_by_id(meeting_id)
        if meeting:
            self.session.delete(meeting)
            self.session.commit()
