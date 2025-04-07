from sqlalchemy import ForeignKey, Integer, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime

from app.database.db import Base

class Evaluation(Base):
    __tablename__ = "evaluations"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    evaluator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    score_timeliness: Mapped[int]
    score_quality: Mapped[int]
    score_completeness: Mapped[int]

    comment: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    task = relationship("Task", back_populates="evaluation")
    evaluator = relationship("User")
