from typing import Optional
from sqlalchemy.orm import Session

from app.models.team import Team
from app.repositories.team.base import TeamsRepository


class SQLAlchemyTeamsRepository(TeamsRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_name(self, name: str) -> Optional[Team]:
        return self.session.query(Team).filter(Team.name == name).first()

    def get_by_invite_code(self, invite_code: str) -> Optional[Team]:
        return self.session.query(Team).filter(Team.invite_code == invite_code).first()

    def add(self, model: Team) -> Team:
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def get(self, oid: str) -> Optional[Team]:
        return self.session.query(Team).filter(Team.id == oid).first()

    def update(self, oid: str, model: Team) -> Team:
        existing_user = self.get(oid)
        if not existing_user:
            return None

        for key, value in model.__dict__.items():
            if value is not None:
                setattr(existing_user, key, value)

        self.session.commit()
        self.session.refresh(existing_user)
        return existing_user

    def list(self, start: int = 0, limit: int = 10) -> list[Team]:
        return self.session.query(Team).offset(start).limit(limit).all()
