from pydantic import BaseModel
from typing import Optional

from app.schemas.team import TeamResponse
from app.schemas.user import UserResponse

class DepartmentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    team_id: int
    manager_id: int

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    manager_id: Optional[int] = None

class DepartmentResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    team: TeamResponse
    manager: Optional[UserResponse] = None

    class Config:
        from_attributes = True
