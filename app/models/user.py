from typing import Optional
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.database.db import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(30))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))

        # Добавляем связи
    team = relationship("Team", back_populates="users")
    role = relationship("Role", back_populates="users")