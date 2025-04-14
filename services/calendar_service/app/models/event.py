from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.db import Base


class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    id = Column(Integer, primary_key=True)
    calendar_id = Column(Integer, ForeignKey("calendars.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    is_meeting = Column(Boolean, default=False)
    task_id = Column(Integer, nullable=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=True)

    meeting = relationship("Meeting", back_populates="events")

    calendar = relationship("Calendar", back_populates="events")