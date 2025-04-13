from pydantic import BaseModel
from typing import List, Optional

from app.schemas.user import UserSummary
from app.schemas.department import DepartmentStructure


class TeamCreate(BaseModel):
    name: str
    description: Optional[str] = None

# Схема для ответа при создании команды
class TeamResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True  # чтобы Pydantic мог работать с SQLAlchemy моделями

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class TeamStructureResponse(BaseModel):
    team_id: int
    team_name: str
    admins: List[UserSummary]
    departments: List[DepartmentStructure]
    members_without_department: List[UserSummary]
