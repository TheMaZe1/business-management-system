# app/schemas/department.py

from pydantic import BaseModel
from typing import List, Optional

from app.schemas.user import UserSummary


class DepartmentCreate(BaseModel):
    team_id: int
    name: str
    description: Optional[str] = None


class DepartmentResponse(BaseModel):
    id: int
    team_id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class DepartmentStructure(BaseModel):
    department_id: int
    name: str
    managers: List[UserSummary]
    members: List[UserSummary]