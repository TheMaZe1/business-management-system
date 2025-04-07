from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.evaluation import EvaluationCreate, EvaluationResponse, AverageScoreResponse
from app.services.evaluation import EvaluationService
from app.database.db import get_db

router = APIRouter(prefix="/evaluations", tags=["Evaluations"])

@router.post("/evaluate", response_model=EvaluationResponse)
def evaluate_task(
    data: EvaluationCreate,
    evaluator_id: int = 1,  # пока без аутентификации
    service: EvaluationService = Depends(EvaluationService)
):
    try:
        return service.evaluate(evaluator_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/{user_id}", response_model=list[EvaluationResponse])
def get_user_evaluations(
    user_id: int,
    service: EvaluationService = Depends(EvaluationService),
):
    try:
        return service.get_user_evaluations(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/user/{user_id}/average", response_model=AverageScoreResponse)
def get_user_average_score(
    user_id: int,
    service: EvaluationService = Depends(EvaluationService),
):
    try:
        return service.get_user_average(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
