import datetime
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound

from app.models.user import User


class SQLAlchemyUsersRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_fullname(self, surname: str, name: str) -> Optional[User]:
        stmt = select(User).where(User.surname == surname, User.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, model: User) -> User:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def get_by_id(self, oid: str) -> Optional[User]:
        stmt = select(User).where(User.id == oid)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, oid: str, user_data: dict) -> Optional[User]:
        user = await self.get_by_id(oid)
        if not user:
            return None

        for key, value in user_data.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def soft_delete(self, oid: str) -> Optional[User]:
        user = await self.get_by_id(oid)
        if not user:
            return None
        user.is_deleted = True
        user.deleted_at = datetime.datetime.now()
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def restore(self, oid: str, restore_window_days: int = 7) -> Optional[User]:
        user = await self.get_by_id(oid)
        if not user or not user.is_deleted:
            return None

        if datetime.datetime.now() - user.deleted_at > datetime.timedelta(days=restore_window_days):
            return None

        user.is_deleted = False
        user.deleted_at = None
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_team_id(self, team_id: int) -> List[User]:
        stmt = select(User).where(User.team_id == team_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def list(self, start: int = 0, limit: int = 10) -> List[User]:
        stmt = select(User).offset(start).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()
