from fastapi import APIRouter
from app.api.v1.routers.team import router as team_router
from app.api.v1.routers.members import router as members_router
from app.api.v1.routers.department import router as department_router

router = APIRouter()
router.include_router(team_router)
router.include_router(members_router)
router.include_router(department_router)