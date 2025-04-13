# app/api/v1/routers/members.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.membership import MembershipCreate, MembershipSummary, MembershipUpdate
from app.services.membership import MembershipService
from app.api.v1.routers.deps import get_current_user, get_membership
from app.models.membership import MembershipRole

router = APIRouter(prefix="/teams/{team_id}/members", tags=["Team Members"])

# Получение списка участников команды
@router.get("/", response_model=list[MembershipSummary])
async def get_team_members(team_id: int, service: MembershipService = Depends(MembershipService), current_user: int = Depends(get_current_user)):
    try:
        await get_membership(team_id, current_user, service)
        return await service.get_members_by_team(team_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    pass

@router.post("/{user_id}", response_model=MembershipSummary)
async def add_member(
    team_id: int,
    member_data: MembershipCreate = Depends(),
    service: MembershipService = Depends(MembershipService),  # Сервис для работы с участниками команды
    current_user: int = Depends(get_current_user)  # Текущий аутентифицированный пользователь
):
    try:
        # Проверяем, что текущий пользователь является администратором или имеет права на добавление участников
        membership = await get_membership(team_id, current_user, service)
        
        if membership.role != MembershipRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can add members")

        # Проверяем, что пользователь еще не является участником команды
        existing_membership = await service.get_member_by_team_and_user(team_id, member_data.user_id)
        if existing_membership:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already a member of this team")
        
        # Создаем новое членство
        new_membership = await service.add_member(team_id=team_id, user_id=member_data.user_id, role=member_data.role, department_id=member_data.department_id)
        return new_membership
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# Получение информации об одном участнике
@router.get("/{user_id}", response_model=MembershipSummary)
async def get_member(team_id: int, user_id: int, service: MembershipService = Depends(MembershipService), current_user: int = Depends(get_current_user)):
    try:
        await get_membership(team_id, current_user, service)
        return await service.get_member_by_team_and_user(team_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Изменение роли участника в команде
@router.patch("/{user_id}", response_model=MembershipSummary)
async def update_member_role(team_id: int, user_id: int, membership_data: MembershipUpdate, service: MembershipService = Depends(MembershipService), current_user: int = Depends(get_current_user)):
    try:
        membership = await get_membership(team_id, current_user, service)
        if membership.role != MembershipRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a member of this team")
        return await service.update_member_role(team_id, user_id, membership_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Удаление участника из команды
@router.delete("/{user_id}", status_code=204)
async def delete_member(team_id: int, user_id: int, service: MembershipService = Depends(MembershipService), current_user: int = Depends(get_current_user)):
    try:
        await service.delete_member(team_id, user_id)
        return {"detail": "Member deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
