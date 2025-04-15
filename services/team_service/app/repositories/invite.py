import secrets
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.invite import InviteCode


class InviteCodeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_invite_code(self, team_id: int, expires_at: datetime) -> InviteCode:
        code = secrets.token_urlsafe(8)

        invite = InviteCode(
            code=code,
            team_id=team_id,
            expires_at=expires_at
        )
        self.session.add(invite)
        await self.session.commit()
        await self.session.refresh(invite)
        return invite

    async def get_by_code(self, code: str) -> InviteCode | None:
        async with self.session.begin():
            result = await self.session.execute(
                select(InviteCode).where(InviteCode.code == code)
            )
            return result.scalar_one_or_none()
