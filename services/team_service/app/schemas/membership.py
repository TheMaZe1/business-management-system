from typing import Optional

from pydantic import BaseModel

from app.models.membership import MembershipRole

class MembershipCreate(BaseModel):
    user_id: int
    role: MembershipRole
    department_id: Optional[int] = None


class MembershipUpdate(BaseModel):
    role: Optional[MembershipRole] = None  # Обновляем только роль, если нужно
    department_id: Optional[int] = None

    class Config:
        use_enum_values = True  # Это важно для сериализации Enum как строк


class MembershipSummary(BaseModel):
    user_id: int
    role: MembershipRole
    department_id: Optional[int] = None

    class Config:
        from_attributes = True
