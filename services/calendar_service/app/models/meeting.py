# Таблица для связи many-to-many между Meeting и User


from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from app.database.db import Base

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    organizer_id = Column(Integer)
    team_id = Column(Integer, nullable=False)

    events = relationship("CalendarEvent", back_populates="meeting", cascade="all, delete-orphan")