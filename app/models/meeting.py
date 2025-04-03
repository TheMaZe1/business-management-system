from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.database.db import Base
from app.models.user import User

# Промежуточная таблица для связи "многие ко многим" (участники встреч)
meeting_participants = Table(
    "meeting_participants",
    Base.metadata,
    Column("meeting_id", ForeignKey("meetings.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)

class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Добавляем связи
    created_by = relationship("User", foreign_keys=[created_by_id])
    participants = relationship("User", secondary=meeting_participants, backref="meetings")
