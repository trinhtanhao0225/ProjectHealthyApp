# backend/modules/exercise/calorie_estimator.py
import math
from backend.utils.logger import logger
from backend.modules.exercise.info_retriever import get_exercise_by_name
def estimate_calories_by_name_only(filter_obj, exercise_name: str, sets: int, reps: int, weight_kg: float = 70, avg_seconds_per_rep: int = 3):
    """
    Tính calories dựa trên tên bài tập + sets × reps
    """
    info = get_exercise_by_name(filter_obj,exercise_name)

    if info is None:
        return {
            "status": "error",
            "message": f"Không tìm thấy bài tập: {exercise_name}"
        }

    MET = info["MET"]
    total_reps = sets * reps
    total_seconds = total_reps * avg_seconds_per_rep
    total_hours = total_seconds / 3600
    calories = MET * weight_kg * total_hours

    return {
        "exercise_name": info["name"],
        "sets": sets,
        "reps": reps,
        "MET": MET,
        "total_reps": total_reps,
        "time_seconds": total_seconds,
        "calories": round(calories, 2)
    }