from fastapi import APIRouter
from app.api.v1.routers.task import router as task_router
from app.api.v1.routers.evaluation import router as evaluation_router

router = APIRouter()
router.include_router(task_router)
router.include_router(evaluation_router)
