from enum import Enum
from typing import Optional
from sqlalchemy import Column, String, Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.database.db import Base


class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    STAFF = "staff"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    last_name: Mapped[str] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(30))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    role = Column(SQLAlchemyEnum(UserRole), nullable=False, default=UserRole.STAFF)

        # Добавляем связи
    team = relationship("Team", back_populates="users")