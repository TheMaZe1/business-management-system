from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Boolean, String, func

from app.database.db import Base
from app.models.membership import Membership


class Team(Base):
    __tablename__ = "teams"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    deleted_at: Mapped[datetime] = mapped_column(nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    memberships: Mapped[list[Membership]] = relationship("Membership", back_populates="team")
    departments = relationship("Department", back_populates="team")
    news = relationship("TeamNews", back_populates="team")
    invite_codes = relationship("InviteCode", back_populates="team", cascade="all, delete-orphan")