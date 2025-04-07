from fastapi import APIRouter
from app.api.routers.user import router as user_router
from app.api.routers.team import router as team_router
from app.api.routers.department import router as department_router
from app.api.routers.task import router as task_router
from app.api.routers.meeting import router as meeting_router
from app.api.routers.news import router as news_router

router = APIRouter()
router.include_router(user_router)
router.include_router(team_router)
router.include_router(department_router)
router.include_router(task_router)
router.include_router(meeting_router)
router.include_router(news_router)