from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, String

from app.database.db import Base


class Team(Base):
    __tablename__ = "teams"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    invite_code: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(255))

    users = relationship("User", back_populates="team")
    departments = relationship("Department", back_populates="team")
