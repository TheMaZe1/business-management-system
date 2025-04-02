from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String

from app.database.db import Base


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    users = relationship("User", back_populates="role")