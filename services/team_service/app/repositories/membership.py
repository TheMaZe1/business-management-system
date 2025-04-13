from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from app.models.membership import Membership
from typing import Optional
from app.models.team import Team

class SQLAlchemyMembershipRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, membership: Membership) -> Membership:
        self.session.add(membership)
        await self.session.commit()
        await self.session.refresh(membership)
        return membership

    async def get_by_user_and_team(self, user_id: int, team_id: int) -> Optional[Membership]:
        async with self.session.begin():
            result = await self.session.execute(
                select(Membership).filter(Membership.user_id == user_id, Membership.team_id == team_id)
            )
            return result.scalars().first()

    async def list_by_team(self, team_id: int) -> list[Membership]:
        result = await self.session.execute(
            select(Membership).filter(Membership.team_id == team_id)
        )
        return result.scalars().all()

    async def delete(self, membership: Membership) -> None:
        await self.session.delete(membership)
        await self.session.commit()

    async def list_by_department(self, team_id: int, department_id: int) -> list[Membership]:
        result = await self.session.execute(
            select(Membership).filter(
                Membership.team_id == team_id,
                Membership.department_id == department_id
            )
        )
        return result.scalars().all()
