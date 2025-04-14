from fastapi import APIRouter, Depends, HTTPException
from app.services.meeting import MeetingService
from app.schemas.meeting import MeetingCreate, MeetingResponse
from app.api.v1.routers.deps import get_current_user

router = APIRouter(
    prefix="/meetings",
    tags=["Meetings"]
)

# Создать встречу
@router.post("/", response_model=MeetingResponse)
async def create_meeting(
    meeting_data: MeetingCreate,
    current_user: int = Depends(get_current_user),
    service: MeetingService = Depends(MeetingService)
):
    try:
        return await service.create_meeting(meeting_data, created_by=current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Получить все встречи пользователя
@router.get("/", response_model=list[MeetingResponse])
async def get_my_meetings(
    current_user: int = Depends(get_current_user),
    service: MeetingService = Depends(MeetingService)
):
    return await service.get_user_meetings(current_user)


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


# Удалить встречу
@router.delete("/{meeting_id}")
async def delete_meeting(
    meeting_id: int,
    current_user: int = Depends(get_current_user),
    service: MeetingService = Depends(MeetingService)
):
    success = await service.delete_meeting(meeting_id, current_user)
    if not success:
        raise HTTPException(status_code=403, detail="Not allowed or meeting not found")
    return {"detail": "Meeting deleted"}
