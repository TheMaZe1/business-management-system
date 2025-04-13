from fastapi import APIRouter, Depends, HTTPException
from app.schemas.team import TeamCreate, TeamResponse, TeamUpdate
from app.services.team import TeamService


router = APIRouter(prefix="/teams", tags=["Teams"])

@router.post("/", response_model=TeamResponse)
async def register_team(team_data: TeamCreate, service: TeamService = Depends(TeamService)):
    try:
        return await service.add(team_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{team_id}", response_model=TeamResponse)
async def update_team(team_id: int, team_data: TeamUpdate, service: TeamService = Depends(TeamService)):
    try:
        return await service.update(team_id, team_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(team_id: int, service: TeamService = Depends(TeamService)):
    try:
        return await service.get_by_id(team_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{team_id}", status_code=204)
async def soft_delete_team(team_id: int, service: TeamService = Depends(TeamService)):
    try:
        await service.soft_delete_team(team_id)
        return {"detail": "Team deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.post("/restore/{user_id}", response_model=TeamResponse)
async def restore_user(
    team_id: int,
    service: TeamService = Depends(TeamService)
):
    try:
        return await service.restore(team_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
