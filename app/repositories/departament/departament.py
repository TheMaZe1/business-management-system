from sqlalchemy.orm import Session


from app.models.departament import Department
from app.repositories.departament.base import DepartamentsRepository


class SQLAlchemyDepartamentsRepository(DepartamentsRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_by_name(self, name: str) -> Department | None:
        return self.session.query(Department).filter(Department.name == name).first()

    def add(self, model: Department) -> Department:
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def get_by_id(self, oid: str) -> Department | None:
        return self.session.query(Department).filter(Department.id == oid).first()

    def update(self, oid: str, departament_data: dict) -> Department:
        existing_departament = self.get(oid)
        if not existing_departament:
            return None

        for key, value in departament_data.items():
            if value is not None:
                setattr(existing_departament, key, value)

        self.session.commit()
        self.session.refresh(existing_departament)
        return existing_departament

    def list(self, start: int = 0, limit: int = 10) -> list[Department]:
        return self.session.query(Department).offset(start).limit(limit).all()