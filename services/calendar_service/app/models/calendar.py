from sqlalchemy import Boolean, Column, Integer
from sqlalchemy.orm import relationship

from app.database.db import Base


class Calendar(Base):
    __tablename__ = "calendars"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, nullable=False)  # user_id или team_id
    is_team_calendar = Column(Boolean, default=False)

    events = relationship("CalendarEvent", back_populates="calendar")