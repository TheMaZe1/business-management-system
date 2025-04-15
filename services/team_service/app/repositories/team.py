import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.team import Team


class SQLAlchemyTeamsRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_name(self, name: str) -> Optional[Team]:
        async with self.session.begin():
            result = await self.session.execute(select(Team).filter(Team.name == name))
            return result.scalar_one_or_none()

    async def add(self, model: Team) -> Team:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def get_by_id(self, oid: str) -> Optional[Team]:
        async with self.session.begin():
            result = await self.session.execute(select(Team).filter(Team.id == oid))
            return result.scalar_one_or_none()

    async def update(self, oid: str, model: Team) -> Optional[Team]:
        existing_team = await self.get_by_id(oid)
        if not existing_team:
            return None

        # Обновление значений
        for key, value in model.items():
            if value is not None:
                setattr(existing_team, key, value)

        await self.session.commit()
        await self.session.refresh(existing_team)
        return existing_team

    async def soft_delete(self, oid: str) -> None:
        team = await self.get_by_id(oid)
        if not team:
            return None
        team.is_deleted = True
        team.deleted_at = datetime.datetime.now()
        await self.session.commit()
        await self.session.refresh(team)
        return team
    
    async def restore(self, oid: str, restore_window_days: int = 7) -> Optional[Team]:
        team = await self.get_by_id(oid)
        if not team or not team.is_deleted:
            return None

        if datetime.datetime.now() - team.deleted_at > datetime.timedelta(days=restore_window_days):
            return None

        team.is_deleted = False
        team.deleted_at = None
        await self.session.commit()
        await self.session.refresh(team)
        return team

    async def list(self, start: int = 0, limit: int = 10) -> list[Team]:
        async with self.session.begin():
            result = await self.session.execute(select(Team).offset(start).limit(limit))
            return result.scalars().all()
