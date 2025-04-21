from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.department import Department



class SQLAlchemyDepartmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, department: Department) -> Department:
        self.session.add(department)
        await self.session.commit()
        await self.session.refresh(department)
        return department

    async def get_by_id(self, department_id: int) -> Optional[Department]:
        result = await self.session.execute(
            select(Department).where(Department.id == department_id)
        )
        return result.scalars().first()

    async def get_by_team(self, team_id: int) -> List[Department]:
        result = await self.session.execute(
            select(Department).where(Department.team_id == team_id)
        )
        return result.scalars().all()

    async def delete(self, department: Department) -> None:
        await self.session.delete(department)
        await self.session.commit()


    async def list_by_team(self, team_id: int) -> list[Department]:
        async with self.session.begin():
            result = await self.session.execute(
                select(Department).where(Department.team_id == team_id)
            )
            return result.scalars().all()