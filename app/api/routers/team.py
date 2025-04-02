from fastapi import APIRouter, Depends, HTTPException
from app.schemas.team import TeamCreate, TeamResponse, TeamUpdate
from app.services.team import TeamService


router = APIRouter(prefix="/teams", tags=["Teams"])

@router.post("/", response_model=TeamResponse)
def register_team(team_data: TeamCreate = Depends, service: TeamService = Depends(TeamService)):
    try:
        return service.add(team_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{team_id}", response_model=TeamResponse)
def update_user(team_id: int, team_data: TeamUpdate, service: TeamService = Depends(TeamService)):
    try:
        return service.update(team_id, team_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{team_id}", response_model=TeamResponse)
def get_user(team_id: int, service: TeamService = Depends(TeamService)):
    try:
        return service.get_by_id(team_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
