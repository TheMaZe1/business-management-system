from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.models.team import Team
from app.repositories.team import SQLAlchemyTeamsRepository
from app.schemas.team import TeamCreate, TeamResponse, TeamStructureResponse, TeamUpdate
from app.database.db import get_db_session
from app.models.membership import Membership, MembershipRole
from app.repositories.membership import SQLAlchemyMembershipRepository
from app.schemas.department import DepartmentStructure
from app.schemas.user import UserSummary
from app.repositories.department import SQLAlchemyDepartmentRepository


class TeamService:
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.team_repo = SQLAlchemyTeamsRepository(db)
        self.membership_repo = SQLAlchemyMembershipRepository(db)
        self.department_repo = SQLAlchemyDepartmentRepository(db)

    async def _create_membership(self, user_id: int, team_id: int):
        # Создаем запись в таблице Membership для связи пользователя и команды
        membership = Membership(
            user_id=user_id,
            team_id=team_id,
            role=MembershipRole.ADMIN, 
        )
        
        # Добавляем membership в репозиторий
        await self.membership_repo.add(membership)

    async def add(self, team_data: TeamCreate, user_id: int) -> TeamResponse:
        existing_team = await self.team_repo.get_by_name(team_data.name)
        if existing_team:
            raise ValueError("Team with this name already exists")

        team = Team(
            name=team_data.name,
            description=team_data.description,
        )

        new_team = await self.team_repo.add(team)

        await self._create_membership(user_id, new_team.id)

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
    
    async def get_team_structure(self, team_id: int) -> TeamStructureResponse:
        team = await self.team_repo.get_by_id(team_id)
        if not team:
            raise ValueError("Team not found")

        memberships = await self.membership_repo.list_by_team(team_id)
        departments = await self.department_repo.list_by_team(team_id)

        admins = []
        members_without_department = []
        department_map = {dept.id: {"managers": [], "members": []} for dept in departments}

        for m in memberships:
            user = m.user_id
            user_summary = UserSummary(user_id=user)

            if m.role == MembershipRole.ADMIN:
                admins.append(user_summary)

            elif m.department_id is None:
                members_without_department.append(user_summary)

            elif m.department_id in department_map:
                if m.role == MembershipRole.MANAGER:
                    department_map[m.department_id]["managers"].append(user_summary)
                else:
                    department_map[m.department_id]["members"].append(user_summary)

        dept_structures = [
            DepartmentStructure(
                department_id=dept.id,
                name=dept.name,
                managers=department_map[dept.id]["managers"],
                members=department_map[dept.id]["members"]
            )
            for dept in departments
        ]

        return TeamStructureResponse(
            team_id=team.id,
            team_name=team.name,
            admins=admins,
            departments=dept_structures,
            members_without_department=members_without_department
        )