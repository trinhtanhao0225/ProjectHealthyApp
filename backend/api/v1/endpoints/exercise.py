from fastapi import APIRouter, Body, Query
from typing import List, Optional
from backend.models.exercise_detail import ExerciseDetail
from backend.models.workout_plan import WorkoutPlan
from backend.schemas.exercise import (
    ExerciseGroupCreate,
    ExerciseGroupResponse,
    ExerciseDetailResponse,       # Giả sử bạn có schema này cho detail
    WorkoutPlanResponse,
    ExercisesResponse,            # Nếu có, dùng cho list detail
)
from backend.services.exercise_service import ExerciseService

router = APIRouter(tags=["Exercise"])

service = ExerciseService()


# ----------------- GROUP -----------------
@router.post("/group", response_model=ExerciseGroupResponse)
async def add_group(payload: ExerciseGroupCreate):
    await service.addExerciseGroup(payload.email, payload.group_name)
    return ExerciseGroupResponse(email=payload.email, group_name=payload.group_name)


@router.get("/groups")
async def get_groups(email: str = Query(..., description="Email người dùng")):
    groups = await service.getGroupsByEmail(email)
    
    # Fix ObjectId → str thủ công (không sửa schema)
    fixed_groups = []
    for group in groups:
        fixed = group.copy()  # tránh modify dict gốc
        if "_id" in fixed:
            fixed["id"] = str(fixed.pop("_id"))  # rename _id -> id và convert str
        fixed_groups.append(fixed)
    
    return fixed_groups




# ----------------- DETAIL -----------------
@router.post("/detail", response_model=dict)  # Có thể thay bằng schema nếu cần
async def add_detail(payload: ExerciseDetail = Body(...)):
    print("=== BODY /detail NHẬN ĐƯỢC ===")
    print(payload.dict())
    
    await service.addExerciseDetail(
        payload.email,
        payload.group_name,
        payload.name,
        payload.sets,
        payload.reps
    )
    return {"exercise": payload.name, "message": "Thêm bài tập thành công"}


@router.get("/detail", response_model=ExercisesResponse)  # Hoặc List[ExerciseDetailResponse]
async def get_detail(
    email: str = Query(..., description="Email người dùng"),
    group_name: str = Query(..., description="Tên nhóm bài tập")
):
    details = await service.getExercisesByEmailAndGroup(email, group_name)
    return {"success": True, "data": details}


# ----------------- PLAN -----------------
@router.post("/plans", response_model=dict)  # Nên thay bằng WorkoutPlanResponse nếu phù hợp
async def add_plan(data: WorkoutPlan):
    result = await service.addExercisePlan(data)
    return result


@router.get("/plans")
async def get_plan(
    email: str = Query(..., description="Email người dùng"),
    day: Optional[str] = Query(None, description="Ngày (YYYY-MM-DD), nếu không truyền thì lấy tất cả")
):
    if day:
        plans = await service.getPlansByEmailAndDay(email, day)
    else:
        plans = await service.getPlansByEmail(email)
    
    # Fix tương tự cho plans
    fixed_plans = []
    for plan in plans:
        fixed = plan.copy()
        if "_id" in fixed:
            fixed["id"] = str(fixed.pop("_id"))
        fixed_plans.append(fixed)
    
    return fixed_plans

@router.put("/plan/done", response_model=dict)
async def done_plan(
    email: str = Query(...),
    group_name: str = Query(...),
    day: str = Query(...),
    session: str = Query(...)
):
    result = await service.updateDoneFlag(email, group_name, day, session)
    return result


# ----------------- DATASET & FILTER -----------------
@router.get("/filter")
async def filter_exercises(
    category: Optional[str] = Query(None),
    equipment: Optional[str] = Query(None),
    muscle: Optional[str] = Query(None)
):
    return await service.filterExercises(category, equipment, muscle)  # thêm await nếu là async


@router.get("/exercise-info", response_model=dict)
async def exercise_info(name: str = Query(..., description="Tên bài tập")):
    info = service.getExerciseInfoByName(name)
    if info is None:
        return {"success": False, "message": "Không tìm thấy bài tập"}
    return {"success": True, "data": info}


@router.post("/calculate-calories", response_model=dict)
async def calculate_calories(
    name: str = Body(...),
    weight: float = Body(...),
    duration: int = Body(...)
):
    result = service.estimateCaloriesByName(name, weight, duration)
    if result is None:
        return {"success": False, "message": "Không tìm thấy bài tập"}
    return {"success": True, "data": result}


@router.get("/muscles")
async def get_muscles():
    return service.getMuscles()


@router.get("/equipment")
async def get_equipment():
    return service.getEquipment()


@router.get("/dependent-filters")
async def dependent_filters(muscle: str = Query(...)):
    return service.getDependentFilters(muscle)


# ----------------- GROUP EXERCISES (đã fix) -----------------
@router.get("/group/exercises", response_model=ExercisesResponse)  # hoặc dict nếu chưa có schema
async def get_exercises_by_group(
    email: str = Query(..., description="Email người dùng"),
    group_name: str = Query(..., description="Tên nhóm")
):
    """
    Lấy danh sách bài tập chi tiết theo email và tên nhóm.
    Response format nhất quán: {"success": bool, "data": list}
    """
    exercises = await service.getExercisesByEmailAndGroup(email, group_name)
    return {"success": True, "data": exercises}