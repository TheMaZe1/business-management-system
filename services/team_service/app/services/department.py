from typing import List, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.department import Department
from app.repositories.department import SQLAlchemyDepartmentRepository
from app.database.db import get_db_session


class DepartmentService:
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.repository = SQLAlchemyDepartmentRepository(db)
        
    async def create_department(self, team_id: int, name: str, description: Optional[str] = None) -> Department:
        department = Department(name=name, description=description, team_id=team_id)
        return await self.repository.add(department)

    async def get_department(self, department_id: int) -> Optional[Department]:
        return await self.repository.get_by_id(department_id)

    async def get_departments_by_team(self, team_id: int) -> List[Department]:
        return await self.repository.get_by_team(team_id)

    async def delete_department(self, department_id: int) -> None:
        department = await self.repository.get_by_id(department_id)
        if department:
            await self.repository.delete(department)
        else:
            raise ValueError("Department not found")
