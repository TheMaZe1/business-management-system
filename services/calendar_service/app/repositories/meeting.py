from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.meeting import Meeting

class MeetingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, meeting: Meeting) -> Meeting:
        self.db.add(meeting)
        await self.db.flush()
        return meeting

    async def get_by_id(self, meeting_id: int) -> Meeting | None:
        result = await self.db.execute(
            select(Meeting).where(Meeting.id == meeting_id)
        )
        return result.scalars().first()
