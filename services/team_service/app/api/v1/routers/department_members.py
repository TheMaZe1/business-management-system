from fastapi import APIRouter, Depends, HTTPException, status
from app.services.membership import MembershipService
from app.api.v1.routers.deps import get_current_user, get_membership
from app.schemas.membership import MembershipSummary
from app.models.membership import MembershipRole  # если роли в отдельном файле

router = APIRouter(prefix="/teams/{team_id}/departments/{department_id}/members", tags=["Departments Members"])

@router.post("/{user_id}", response_model=MembershipSummary)
async def add_user_to_department(
    team_id: int,
    department_id: int,
    user_id: int,
    membership_service: MembershipService = Depends(MembershipService),
    current_user: int = Depends(get_current_user)
):
    # Получаем роль текущего пользователя
    member = await get_membership(team_id, current_user, membership_service)

    if not member:
        raise HTTPException(status_code=403, detail="You are not a member of this team")

    # Менеджер может добавлять только в свой отдел
    if member.role == MembershipRole.MANAGER:
        if member.department_id != department_id:
            raise HTTPException(status_code=403, detail="Managers can only add users to their own department")

    elif member.role != MembershipRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins or managers can add users to departments")

    # Добавляем пользователя
    try:
        return await membership_service.assign_user_to_department(team_id, user_id, department_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[MembershipSummary])
async def list_department_members(
    team_id: int,
    department_id: int,
    membership_service: MembershipService = Depends(MembershipService),
    current_user: int = Depends(get_current_user)
):
    await get_membership(team_id, current_user, membership_service)
    return await membership_service.get_members_by_department(team_id, department_id)


@router.get("/{user_id}", response_model=MembershipSummary)
async def get_department_member(
    team_id: int,
    department_id: int,
    user_id: int,
    membership_service: MembershipService = Depends(MembershipService),
    current_user: int = Depends(get_current_user)
):
    await get_membership(team_id, current_user, membership_service)
    member = await membership_service.get_member_by_team_and_user(team_id, user_id)
    if member is None or member.department_id != department_id:
        raise HTTPException(status_code=404, detail="User not found in this department")
    return member