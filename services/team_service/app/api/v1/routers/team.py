from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.team import TeamCreate, TeamResponse, TeamStructureResponse, TeamUpdate
from app.services.team import TeamService
from app.api.v1.routers.deps import get_current_user, get_membership
from app.models.membership import MembershipRole
from app.services.membership import MembershipService


router = APIRouter(prefix="/teams", tags=["Teams"])

@router.post("/", response_model=TeamResponse)
async def register_team(team_data: TeamCreate, service: TeamService = Depends(TeamService), current_user: int = Depends(get_current_user)):
    try:
        return await service.add(team_data, current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{team_id}", response_model=TeamResponse)
async def update_team(team_id: int, team_data: TeamUpdate, service: TeamService = Depends(TeamService), current_user: int = Depends(get_current_user)):
    try:
        membership = await get_membership(team_id, current_user)
        if membership.role != MembershipRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a member of this team")
        return await service.update(team_id, team_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(team_id: int, service: TeamService = Depends(TeamService), current_user: int = Depends(get_current_user), membership_service: MembershipService = Depends(MembershipService)):
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
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a member of this team")
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
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a member of this team")
        return await service.restore(team_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{team_id}/structure", response_model=TeamStructureResponse)
async def get_structure(team_id: int, current_user: int = Depends(get_current_user), service: TeamService = Depends(TeamService), membership_service: MembershipService = Depends(MembershipService)):
    await get_membership(team_id, current_user, membership_service)  # Проверка членства
    try:
        return await service.get_team_structure(team_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))