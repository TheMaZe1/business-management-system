from fastapi import APIRouter, Depends, HTTPException, Request

from app.services.meeting import MeetingService
from app.schemas.meeting import MeetingCreate, MeetingResponse, MeetingUpdate
from app.api.v1.routers.deps import get_current_user, get_meeting_service, get_membership
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
    service: MeetingService = Depends(get_meeting_service)
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
    service: MeetingService = Depends(get_meeting_service)
):
    member = await get_membership(team_id, current_user, request)
    if member.role not in [MembershipRole.ADMIN, MembershipRole.MANAGER]:
               # Если пользователь не админ или менеджер, проверяем, есть ли он в участниках встречи
        meetings = await service.get_meetings_by_team(team_id)
        accessible_meetings = [
            meeting for meeting in meetings if current_user in meeting.participant_ids
        ]
        if not accessible_meetings:
            raise HTTPException(status_code=403, detail="You do not have access to any meetings in this team")

        return accessible_meetings
    return await service.get_meetings_by_team(team_id)


# Получить встречу по ID
@router.get("/{meeting_id}", response_model=MeetingResponse)
async def get_meeting(
    meeting_id: int,
    current_user: int = Depends(get_current_user),
    service: MeetingService = Depends(get_meeting_service)
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
    service: MeetingService = Depends(get_meeting_service)
):
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
    service: MeetingService = Depends(get_meeting_service)
):
    meeting = await service.get_meeting_by_id(meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    if meeting.organizer_id != current_user:
        raise HTTPException(status_code=403, detail="Only the organizer can delete this meeting")

    await service.delete_meeting(meeting_id, current_user)
    return meeting
