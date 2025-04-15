from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.team import TeamCreate, TeamResponse, TeamStructureResponse, TeamUpdate
from app.services.team import TeamService
from app.api.v1.routers.deps import get_current_user, get_membership
from app.models.membership import MembershipRole
from app.services.membership import MembershipService
from app.schemas.invite import InviteCodeResponse
from app.services.invite import InviteService
from app.schemas.membership import MembershipSummary


router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("/", response_model=TeamResponse)
async def register_team(
    team_data: TeamCreate, 
    service: TeamService = Depends(TeamService), 
    current_user: int = Depends(get_current_user)):
    try:
        return await service.add(team_data, current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{team_id}", response_model=TeamResponse)
async def update_team(
    team_id: int, 
    team_data: TeamUpdate, 
    service: TeamService = Depends(TeamService), 
    current_user: int = Depends(get_current_user), 
    membership_service: MembershipService = Depends(MembershipService)):
    try:
        membership = await get_membership(team_id, current_user, membership_service)
        if membership.role != MembershipRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the admin can update team")
        return await service.update(team_id, team_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(
    team_id: int, 
    service: TeamService = Depends(TeamService), 
    current_user: int = Depends(get_current_user), 
    membership_service: MembershipService = Depends(MembershipService)):
    try:
        await get_membership(team_id, current_user, membership_service)
        return await service.get_by_id(team_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{team_id}", status_code=204)
async def soft_delete_team(
    team_id: int,
    service: TeamService = Depends(TeamService),
    current_user: int = Depends(get_current_user),
    membership_service: MembershipService = Depends(MembershipService)):
    try:
        membership = await get_membership(team_id, current_user, membership_service)
        if membership.role != MembershipRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the admin can delete team")
        await service.soft_delete_team(team_id)
        return {"detail": "Team deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.post("/restore/{user_id}", response_model=TeamResponse)
async def restore_user(
    team_id: int,
    service: TeamService = Depends(TeamService),
    current_user: int = Depends(get_current_user),
    membership_service: MembershipService = Depends(MembershipService)
):
    try:
        membership = await get_membership(team_id, current_user, membership_service)
        if membership.role != MembershipRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the admin can restore team")
        return await service.restore(team_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{team_id}/structure", response_model=TeamStructureResponse)
async def get_structure(
    team_id: int, 
    current_user: int = Depends(get_current_user), 
    service: TeamService = Depends(TeamService), 
    membership_service: MembershipService = Depends(MembershipService)):
    await get_membership(team_id, current_user, membership_service)  # Проверка членства
    try:
        return await service.get_team_structure(team_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{team_id}/invite", response_model=InviteCodeResponse)
async def create_invite_code(
    team_id: int,
    service = Depends(InviteService),
    current_user: int = Depends(get_current_user),
    membership_service: MembershipService = Depends(MembershipService)
):
    try:
        membership = await get_membership(team_id, current_user, membership_service)
        if membership.role != MembershipRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the admin can create invite code team")
        invite = await service.generate_invite_code(team_id)
        return invite
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/join/{invite_code}", response_model=MembershipSummary)
async def join_team_by_invite(
    invite_code: str,
    service: MembershipService = Depends(MembershipService),
    invite_service: InviteService = Depends(InviteService),
    current_user: int = Depends(get_current_user),
):
    try:
        # Получаем инвайт по коду и валидируем
        invite = await invite_service.get_invite(invite_code)
        team_id = invite.team_id

        # Проверяем, не состоит ли уже юзер в команде
        existing = await service.get_member_by_team_and_user(team_id, current_user)
        if existing:
            raise HTTPException(status_code=400, detail="You are already a member of this team")

        # Добавляем пользователя с дефолтной ролью
        new_member = await service.add_member(
            team_id=team_id,
            user_id=current_user,
            role=MembershipRole.STAFF, 
            department_id=None
        )

        return new_member

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))