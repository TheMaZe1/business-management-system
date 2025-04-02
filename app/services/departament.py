from sqlalchemy.orm import Session
from app.models.departament import Department
from app.models.user import User
from app.repositories.departament.departament import SQLAlchemyDepartamentsRepository
from app.repositories.team.team import SQLAlchemyTeamsRepository
from app.repositories.user.user import SQLAlchemyUsersRepository
from app.schemas.departament import DepartmentCreate, DepartmentResponse, DepartmentUpdate
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from fastapi import Depends
from app.database.db import get_db


class DepartamentService:
    def __init__(self, db: Session = Depends(get_db)):
        self.user_repo = SQLAlchemyUsersRepository(db)
        self.departament_repo = SQLAlchemyDepartamentsRepository(db)
        self.team_repo = SQLAlchemyTeamsRepository(db)

    def add(self, departament_data: DepartmentCreate) -> DepartmentResponse:
        existing_departament = self.departament_repo.get_by_name(departament_data.name)
        if existing_departament:
            raise ValueError("Departament with this email already exists")

        team = self.team_repo.get_by_id(departament_data.team_id)
        if not team:
            raise ValueError("Invalid team id")
        
        manager = self.user_repo.get_by_id(departament_data.manager_id)
        if not manager:
            raise ValueError("Invalid manager id")
        
        departament = Department(
            name=departament_data.name,
            description=departament_data.description,
            team=team,
            manager=manager,
        )

        return DepartmentResponse.model_validate(self.departament_repo.add(departament))

    def update(self, department_id: int, department_data: DepartmentUpdate) -> DepartmentResponse:
        department = self.departament_repo.get_by_id(department_id)
        if not department:
            raise ValueError("Department not found")

        # Проверяем, занят ли email
        if department_data.name:
            existing_department = self.departament_repo.get_by_name(department_data.name)
            if existing_department and existing_department.id != department_id:
                raise ValueError("Name of department is already in use")

        return DepartmentResponse.model_validate(self.departament_repo.update(department_id, department_data.model_dump(exclude_unset=True)))
    
    def get_by_name(self, name: str) -> DepartmentResponse:
        existing_department = self.department_repo.get_by_name(name)
        if existing_department:
            return DepartmentResponse.model_validate(existing_department)
        else:
            raise ValueError("Department not found")
        
    def get_by_id(self, oid: str) -> DepartmentResponse:
        existing_department = self.departament_repo.get_by_id(oid)
        if existing_department:
            return DepartmentResponse.model_validate(existing_department)
        else:
            raise ValueError("Department not found")