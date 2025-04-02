from sqlalchemy.orm import Session
from app.models.team import Team
from app.repositories.team.team import SQLAlchemyTeamsRepository
from app.schemas.team import TeamCreate, TeamResponse, TeamUpdate
from fastapi import Depends
from app.database.db import get_db


class TeamService:
    def __init__(self, db: Session = Depends(get_db)):
        self.team_repo = SQLAlchemyTeamsRepository(db)

    def add(self, team_data: TeamCreate) -> TeamResponse:
        existing_team = self.team_repo.get_by_name(team_data.name)
        if existing_team:
            raise ValueError("Team with this name already exists")
        
        team = Team(
            name=team_data.name,
            description=team_data.description,
            invite_code=team_data.invite_code
        )

        return TeamResponse.model_validate(self.team_repo.add(team))

    def update(self, team_id: int, team_data: TeamUpdate) -> TeamResponse:
        team = self.team_repo.get_by_id(team_id)
        if not team:
            raise ValueError("Team not found")

        # Проверяем, занят ли email
        if team_data.name:
            existing_team = self.team_repo.get_by_name(team_data.name)
            if existing_team and existing_team.id != team_id:
                raise ValueError("Name is already in use")

        return TeamResponse.model_validate(self.team_repo.update(team_id, team_data.model_dump(exclude_unset=True)))
    
    def get_by_name(self, name: str) -> TeamResponse:
        existing_team = self.team_repo.get_by_name(name)
        if existing_team:
            return TeamResponse.model_validate(existing_team)
        else:
            raise ValueError("Team not found")
        
    def get_by_id(self, oid: str) -> TeamResponse:
        existing_team = self.team_repo.get_by_id(oid)
        if existing_team:
            return TeamResponse.model_validate(existing_team)
        else:
            raise ValueError("Team not found")