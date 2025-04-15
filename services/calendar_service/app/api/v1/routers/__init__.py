from fastapi import APIRouter
from app.api.v1.routers.calendar import router as calendar_router
from app.api.v1.routers.event import router as event_router
from app.api.v1.routers.meeting import router as meeting_router

router = APIRouter()
router.include_router(calendar_router)
router.include_router(event_router)
router.include_router(meeting_router)
