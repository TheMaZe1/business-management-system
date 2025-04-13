# app/services/membership.py

from typing import List

from fastapi import Depends
from app.repositories.membership import SQLAlchemyMembershipRepository
from app.schemas.membership import MembershipSummary, MembershipUpdate
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db_session
from app.models.membership import Membership, MembershipRole


class MembershipService:
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.membership_repo = SQLAlchemyMembershipRepository(db)

    async def add_member(self, team_id: int, user_id: int, role: MembershipRole):
        # Создаем нового участника
        new_membership = Membership(user_id=user_id, team_id=team_id, role=role)

        # Сохраняем в репозитории
        await self.membership_repo.add(new_membership)
        return new_membership

    async def get_members_by_team(self, team_id: int) -> List[MembershipSummary]:
        # Получаем всех участников команды
        members = await self.membership_repo.list_by_team(team_id)
        return [MembershipSummary(user_id=member.user_id, role=member.role) for member in members]

    async def get_member_by_team_and_user(self, team_id: int, user_id: int) -> MembershipSummary | None:
        # Получаем информацию о конкретном участнике
        member = await self.membership_repo.get_by_user_and_team(user_id, team_id)
        if not member:
            return None
        return MembershipSummary(user_id=member.user_id, role=member.role)

    async def update_member_role(self, team_id: int, user_id: int, membership_data: MembershipUpdate) -> MembershipSummary:
        # Обновляем роль участника
        member = await self.membership_repo.get_by_user_and_team(user_id, team_id)
        if not member:
            raise ValueError(f"Member with user_id {user_id} not found in team {team_id}")

        member.role = membership_data.role
        await self.membership_repo.add(member)
        return MembershipSummary(user_id=member.user_id, role=member.role)

    async def delete_member(self, team_id: int, user_id: int):
        # Удаляем участника
        member = await self.membership_repo.get_by_user_and_team(user_id, team_id)
        if not member:
            raise ValueError(f"Member with user_id {user_id} not found in team {team_id}")

        await self.membership_repo.delete(member)
