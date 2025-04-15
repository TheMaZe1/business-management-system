from pydantic import BaseModel
from typing import Optional
from enum import Enum

class MembershipRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"

class MembershipResponse(BaseModel):
    user_id: int
    role: MembershipRole
    department_id: Optional[int]
    role: MembershipRole
