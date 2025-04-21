from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.database.db import Base

class TaskEvaluation(Base):
    __tablename__ = 'task_evaluations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    user_id = Column(Integer, nullable=False)  # Оцененный пользователь
    evaluated_by_id = Column(Integer, nullable=False)  # Оценивший пользователь (например, руководитель)
    deadline_score = Column(Float, nullable=False)  # Оценка за срок
    quality_score = Column(Float, nullable=False)   # Оценка за качество
    completeness_score = Column(Float, nullable=False)  # Оценка за полноту выполнения
    evaluation_date = Column(DateTime, default=func.now())

    task = relationship("Task", back_populates="evaluations")

    def average_score(self):
        return (self.deadline_score + self.quality_score + self.completeness_score) / 3