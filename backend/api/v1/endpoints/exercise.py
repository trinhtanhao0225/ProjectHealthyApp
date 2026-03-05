# backend/api/v1/endpoints/exercise.py
from fastapi import APIRouter, HTTPException, Body, Query
from backend.schemas.exercise import ExerciseActionRequest, ExerciseActionResponse
from backend.services.exercise_service import execute_exercise_action

router = APIRouter(prefix="/exercise", tags=["Exercise"])

@router.post("/action", response_model=ExerciseActionResponse)
async def exercise_action(request: ExerciseActionRequest = Body(...)):
    """
    Endpoint tổng hợp tất cả action từ script test_exercise.py cũ
    """
    result = await execute_exercise_action(request.dict())
    return ExerciseActionResponse(**result)