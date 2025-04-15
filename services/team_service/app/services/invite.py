# services/invite_service.py

from datetime import datetime, timedelta

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.invite import InviteCodeRepository
from app.database.db import get_db_session


class InviteService:
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.repo = InviteCodeRepository(db)

    async def generate_invite_code(self, teeam_id: int, expires_in_days: int = 7):
        expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
        return await self.repo.create_invite_code(teeam_id, expires_at)

    async def get_invite(self, code: str):
        invite = await self.repo.get_by_code(code)
        if not invite:
            raise ValueError("Invite not found")
        if invite.expires_at and invite.expires_at < datetime.utcnow():
            raise ValueError("Invite expired")
        return invite
