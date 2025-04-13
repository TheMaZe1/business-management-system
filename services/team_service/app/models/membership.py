from datetime import datetime
import enum
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, func, Enum as SQLAlchemyEnum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.database.db import Base


class MembershipRole(str, enum.Enum):
    ADMIN = "admin"        # Администратор компании
    MANAGER = "manager"    # Менеджер (например, руководитель отдела)
    STAFF = "staff"  # Сотрудник

class Membership(Base):
    __tablename__ = "memberships"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)  # Просто идентификатор пользователя
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey('teams.id'), nullable=False)
    role = Column(SQLAlchemyEnum(MembershipRole), nullable=False, default=MembershipRole.STAFF)
    joined_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Связь с командой
    team = relationship("Team", back_populates="memberships")