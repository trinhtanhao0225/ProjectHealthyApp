# backend/services/exercise_service.py
from fastapi import HTTPException
from typing import Dict, Any, List, Optional

from backend.models.exercise_detail import ExerciseDetail
from backend.models.exercise_group import ExerciseGroup
from backend.models.workout_plan import WorkoutPlan

from backend.modules.exercise.data_loader import ExerciseFilter
from backend.modules.exercise.info_retriever import get_exercise_by_name
from backend.modules.exercise.calorie_estimator import estimate_calories_by_name_only
from backend.modules.exercise.filter_service import filter_exercises
from backend.utils.fix_json import fix_json_value  # nếu có

from backend.utils.logger import logger

# --------------------- Action-based (từ script test_exercise.py cũ) ---------------------
async def execute_exercise_action(action_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Xử lý tất cả action từ script cũ
    Trả về dict giống hệt output script cũ
    """
    engine = ExerciseFilter()
    result = {}

    try:
        action = action_data.get("action")
        logger.info(f"Executing exercise action: {action}")

        if action == "calories_name_only":
            if not action_data.get("exercise_name"):
                raise ValueError("Thiếu exercise_name")
            result = estimate_calories_by_name_only(
                engine,
                action_data["exercise_name"],
                action_data.get("sets", 0),
                action_data.get("reps", 0),
                action_data.get("weight_kg", 70)
            )

        elif action == "muscles":
            all_muscles = sorted({m for lst in engine.df['combined_muscles'] for m in lst})
            result = {"status": "success", "muscle_groups": all_muscles}

        elif action == "equipment":
            all_equipment = sorted({e for lst in engine.df['equipment'] for e in lst})
            result = {"status": "success", "equipment_list": all_equipment}

        elif action == "difficulty":
            all_levels = sorted({int(l) for l in engine.df['cluster_label'].dropna() if str(l).isdigit()})
            result = {"status": "success", "difficulty_list": all_levels}

        elif action == "filter":
            result = filter_exercises(
                engine,
                muscle=action_data.get("muscle"),
                equipment=action_data.get("equipment"),
                level=action_data.get("difficulty")
            )

        elif action == "get_exercise_info":
            if not action_data.get("exercise_name"):
                raise ValueError("Thiếu exercise_name")
            ex_info = get_exercise_by_name(engine, action_data["exercise_name"])
            result = {
                "status": "success" if ex_info else "error",
                "exercise": ex_info,
                "message": "Không tìm thấy" if not ex_info else None
            }

        else:
            raise ValueError("Sai action")

        # Fix JSON nếu cần
        if fix_json_value:
            result = fix_json_value(result)

        logger.info(f"Action {action} completed")
        return result

    except Exception as e:
        logger.error(f"Exercise action error: {str(e)}")
        return {"status": "error", "message": str(e)}

# --------------------- Group ---------------------
async def add_exercise_group(data: dict):
    group = ExerciseGroup(**data)
    await group.insert()
    return group

async def get_group(email: str, group_name: str):
    return await ExerciseGroup.find_one({"email": email, "group_name": group_name})

async def get_groups_by_email(email: str):
    return await ExerciseGroup.find({"email": email}).to_list()

# --------------------- ExerciseDetail ---------------------
async def add_exercise_detail(data: dict):
    detail = ExerciseDetail(**data)
    await detail.insert()
    return detail

async def get_exercise_detail(email: str, group_name: str, name: str):
    return await ExerciseDetail.find_one({"email": email, "group_name": group_name, "name": name})

async def get_exercises_by_email_and_group(email: str, group_name: str):
    return await ExerciseDetail.find({"email": email, "group_name": group_name}).to_list()

# --------------------- Plan ---------------------
async def add_exercise_plan(data: dict):
    plan = WorkoutPlan(**data)
    await plan.insert()
    return plan

async def get_plans_by_email(email: str):
    return await WorkoutPlan.find({"email": email}).to_list()

async def get_plans_by_email_and_day(email: str, day: str):
    return await WorkoutPlan.find({"email": email, "day": day}).to_list()

# --------------------- Mark Done + Calculate Calories ---------------------
async def update_done_flag(email: str, group_name: str, day: str, session: str, weight_kg: float = 70):
    details = await get_exercises_by_email_and_group(email, group_name)
    
    total_calories = 0
    
    for detail in details:
        calo_result = await execute_exercise_action({
            "action": "calories_name_only",
            "exercise_name": detail.name,
            "sets": detail.sets,
            "reps": detail.reps,
            "weight_kg": weight_kg
        })
        if calo_result.get("status") == "success" and calo_result.get("data", {}).get("calories"):
            total_calories += calo_result["data"]["calories"]
    
    logger.info(f"update_done_flag: group={group_name}, exercises={len(details)}, calories={total_calories}")
    
    updated = await WorkoutPlan.find_one_and_update(
        {"email": email, "group_name": group_name, "day": day, "session": session},
        {"$set": {
            "done_flag": True,
            "calories_burned": total_calories
        }},
        return_document=True
    )
    
    if not updated:
        raise HTTPException(404, "Không tìm thấy plan để cập nhật")
    
    return updated