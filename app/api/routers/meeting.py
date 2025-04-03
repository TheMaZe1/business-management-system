from fastapi import APIRouter, Depends, HTTPException
from app.services.meeting import MeetingService
from app.schemas.meeting import MeetingCreate, MeetingUpdate, MeetingResponse

router = APIRouter(prefix="/meetings", tags=["Meetings"])

@router.post("/", response_model=MeetingResponse)
def create_meeting(
    meeting_data: MeetingCreate,
    created_by_id: int,
    service: MeetingService = Depends(MeetingService)
):
    try:
        return service.add(meeting_data, created_by_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{meeting_id}", response_model=MeetingResponse)
def update_meeting(meeting_id: int, meeting_data: MeetingUpdate, service: MeetingService = Depends(MeetingService)):
    try:
        return service.update(meeting_id, meeting_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{meeting_id}", response_model=MeetingResponse)
def get_meeting(meeting_id: int, service: MeetingService = Depends(MeetingService)):
    try:
        return service.get_by_id(meeting_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[MeetingResponse])
def list_meetings(service: MeetingService = Depends(MeetingService), start: int = 0, limit: int = 10):
    return service.list(start, limit)

@router.delete("/{meeting_id}")
def delete_meeting(meeting_id: int, service: MeetingService = Depends(MeetingService)):
    try:
        service.delete(meeting_id)
        return {"message": "Meeting deleted"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
