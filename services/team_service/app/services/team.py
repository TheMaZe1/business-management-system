from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.team import Team
from app.repositories.team import SQLAlchemyTeamsRepository
from app.schemas.team import TeamCreate, TeamResponse, TeamUpdate
from fastapi import Depends
from app.database.db import get_db_session


class TeamService:
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.team_repo = SQLAlchemyTeamsRepository(db)

    async def add(self, team_data: TeamCreate) -> TeamResponse:
        existing_team = await self.team_repo.get_by_name(team_data.name)
        if existing_team:
            raise ValueError("Team with this name already exists")

        team = Team(
            name=team_data.name,
            description=team_data.description,
        )

        return TeamResponse.model_validate(await self.team_repo.add(team))

    async def update(self, team_id: int, team_data: TeamUpdate) -> TeamResponse:
        team = await self.team_repo.get_by_id(team_id)
        if not team:
            raise ValueError("Team not found")

        # Проверяем, занят ли name
        if team_data.name:
            existing_team = await self.team_repo.get_by_name(team_data.name)
            if existing_team and existing_team.id != team_id:
                raise ValueError("Name is already in use")

        return TeamResponse.model_validate(await self.team_repo.update(team_id, team_data.model_dump(exclude_unset=True)))

    async def get_by_name(self, name: str) -> TeamResponse:
        existing_team = await self.team_repo.get_by_name(name)
        if existing_team:
            return TeamResponse.model_validate(existing_team)
        else:
            raise ValueError("Team not found")

    async def get_by_id(self, oid: str) -> TeamResponse:
        existing_team = await self.team_repo.get_by_id(oid)
        if existing_team:
            return TeamResponse.model_validate(existing_team)
        else:
            raise ValueError("Team not found")

    async def soft_delete_team(self, oid: str) -> TeamResponse:
        team = await self.team_repo.soft_delete(oid)
        if not team:
            raise ValueError("Team not found")

        return TeamResponse.model_validate(team)
    
    async def restore(self,oid: str) -> TeamResponse:
        team = await self.team_repo.restore(oid)
        if not team:
            raise ValueError("Team not found or restore window expired")
        return TeamResponse.model_validate(team)