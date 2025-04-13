# app/schemas/membership.py

from typing import Optional
from pydantic import BaseModel

from app.models.membership import MembershipRole

class MembershipUpdate(BaseModel):
    role: Optional[MembershipRole] = None  # Обновляем только роль, если нужно

    class Config:
        use_enum_values = True  # Это важно для сериализации Enum как строк

class MembershipSummary(BaseModel):
    user_id: int
    role: MembershipRole

    class Config:
        orm_mode = True
        # use_enum_values = True  # Это важно для сериализации Enum как строк

