from datetime import datetime
from enum import Enum

from sqlalchemy import Column, String, Enum as SQLAlchemyEnum, Boolean, func
from sqlalchemy.orm import mapped_column, Mapped

from app.database.db import Base


class UserRole(str, Enum):
    SUPERUSER = "supeuser" # возможно добавление superuser в будущем
    USER = "user"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    last_name: Mapped[str] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(128))
    role = Column(SQLAlchemyEnum(UserRole), nullable=False, default=UserRole.USER)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    deleted_at: Mapped[datetime] = mapped_column(nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
