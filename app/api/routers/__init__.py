from fastapi import APIRouter
from app.api.routers.user import router as user_router
from app.api.routers.team import router as team_router

router = APIRouter()
router.include_router(user_router)
router.include_router(team_router)