from fastapi import APIRouter, Depends, HTTPException, Request
from app.services.meeting import MeetingService
from app.schemas.meeting import MeetingCreate, MeetingResponse, MeetingUpdate
from app.api.v1.routers.deps import get_current_user, get_membership
from app.schemas.membership import MembershipRole

router = APIRouter(
    prefix="/teams/{team_id}/meetings",
    tags=["Meetings"]
)

# Создать встречу
@router.post("/", response_model=MeetingResponse)
async def create_meeting(
    request: Request,
    team_id: int,
    meeting_data: MeetingCreate,
    current_user: int = Depends(get_current_user),
    service: MeetingService = Depends(MeetingService)
):
    try:
        member = await get_membership(team_id, current_user, request)
        if member.role not in [MembershipRole.ADMIN, MembershipRole.MANAGER]:
            raise HTTPException(status_code=403, detail="Only admins or managers can create meetings")
        return await service.create_meeting(current_user, team_id, meeting_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Получить все встречи пользователя
@router.get("/", response_model=list[MeetingResponse])
async def get_team_meetings(
    request: Request,
    team_id: int,
    current_user: int = Depends(get_current_user),
    service: MeetingService = Depends(MeetingService)
):
    member = await get_membership(team_id, current_user, request)
    if member.role not in [MembershipRole.ADMIN, MembershipRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Only admins or managers can see meetings")
    return await service.get_meetings_by_team(team_id)

# @router.get("/", response_model=list[MeetingResponse])
# async def get_my_meetings(
#     current_user: int = Depends(get_current_user),
#     service: MeetingService = Depends(MeetingService)
# ):
#     return await service.get_user_meetings(current_user)


# Получить встречу по ID
@router.get("/{meeting_id}", response_model=MeetingResponse)
async def get_meeting(
    meeting_id: int,
    current_user: int = Depends(get_current_user),
    service: MeetingService = Depends(MeetingService)
):
    meeting = await service.get_meeting_by_id(meeting_id)
    if not meeting or current_user not in meeting.participant_ids:
        raise HTTPException(status_code=403, detail="You are not a participant of this meeting")
    return meeting

# Обновить встречу
@router.put("/{meeting_id}", response_model=MeetingResponse)
async def update_meeting(
    meeting_id: int,
    update_data: MeetingUpdate,
    current_user: int = Depends(get_current_user),
    service: MeetingService = Depends(MeetingService)
):
    meeting = await service.get_meeting_by_id(meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    if meeting.organizer_id != current_user:
        raise HTTPException(status_code=403, detail="Only the organizer can update this meeting")

    try:
        updated_meeting = await service.update_meeting(meeting_id, update_data, current_user)
        return updated_meeting
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# Удалить встречу
@router.delete("/{meeting_id}")
async def delete_meeting(
    meeting_id: int,
    current_user: int = Depends(get_current_user),
    service: MeetingService = Depends(MeetingService)
):
    meeting = await service.get_meeting_by_id(meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    if meeting.organizer_id != current_user:
        raise HTTPException(status_code=403, detail="Only the organizer can delete this meeting")

    success = await service.delete_meeting(meeting_id, current_user)
    return {"detail": "Meeting deleted"}
