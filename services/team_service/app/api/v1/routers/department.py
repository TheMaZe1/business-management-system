from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.department import DepartmentCreate, DepartmentResponse, DepartmentUpdate
from app.services.department import DepartmentService
from app.api.v1.routers.deps import get_current_user, get_membership
from app.services.membership import MembershipService
from app.models.membership import MembershipRole


router = APIRouter(prefix="/teams/{team_id}/departments", tags=["Departments"])


@router.post("/", response_model=DepartmentResponse)
async def create_department(
    team_id: int,
    department_data: DepartmentCreate,
    current_user: int = Depends(get_current_user),
    service: DepartmentService = Depends(DepartmentService),
    membership_service: MembershipService = Depends(MembershipService),
):
    member = await get_membership(team_id, current_user, membership_service)
    if member.role != MembershipRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can create department")
    return await service.create_department(team_id, department_data.name, department_data.description)


@router.get("/", response_model=List[DepartmentResponse])
async def list_departments(
    team_id: int,
    current_user: int = Depends(get_current_user),
    service: DepartmentService = Depends(DepartmentService),
    membership_service: MembershipService = Depends(),
):
    member = await get_membership(team_id, current_user, membership_service)
    if member.role != MembershipRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the admin can view departments")
    return await service.get_departments_by_team(team_id)


@router.get("/{department_id}", response_model=DepartmentResponse)
async def get_department(
    team_id: int,
    department_id: int,
    current_user: int = Depends(get_current_user),
    service: DepartmentService = Depends(DepartmentService),
    membership_service: MembershipService = Depends(),
):
    await get_membership(team_id, current_user, membership_service)
    return await service.get_department(department_id)


@router.patch("/{department_id}", response_model=DepartmentResponse)
async def update_department(
    team_id: int,
    department_id: int,
    update_data: DepartmentUpdate,
    current_user: int = Depends(get_current_user),
    service: DepartmentService = Depends(DepartmentService),
    membership_service: MembershipService = Depends(),
):
    member = await get_membership(team_id, current_user, membership_service)
    if member.role != MembershipRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can update department")
    return await service.update_department(department_id, update_data)


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
    team_id: int,
    department_id: int,
    current_user: int = Depends(get_current_user),
    service: DepartmentService = Depends(DepartmentService),
    membership_service: MembershipService = Depends(),
):
    member = await get_membership(team_id, current_user, membership_service)
    if member.role != MembershipRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can delete department")
    await service.delete_department(department_id)
