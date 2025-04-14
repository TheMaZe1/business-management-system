from fastapi import APIRouter
from app.api.v1.routers.task import router as task_router

router = APIRouter()
router.include_router(task_router)
