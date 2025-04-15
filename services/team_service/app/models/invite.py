from datetime import datetime

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, Boolean, DateTime, ForeignKey, Integer, String, func

from app.database.db import Base
from app.models.membership import Membership


class InviteCode(Base):
    __tablename__ = "invite_codes"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)  # опционально, если хочешь срок жизни

    team = relationship("Team", back_populates="invite_codes")