# app/schemas/department.py

from pydantic import BaseModel
from typing import Optional


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