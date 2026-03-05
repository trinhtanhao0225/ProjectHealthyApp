# backend/scripts/test_exercise.py
import sys
import json
from backend.modules.exercise.data_loader import ExerciseFilter
from backend.modules.exercise.info_retriever import get_exercise_by_name  # ← Đã import hàm từ file riêng
from backend.modules.exercise.calorie_estimator import estimate_calories_by_name_only
from backend.modules.exercise.filter_service import filter_exercises
from backend.utils.fix_json import fix_json_value  # sửa tên file nếu bạn dùng fix_json.py


if __name__ == "__main__":
    engine = ExerciseFilter()

    # Lấy input từ stdin hoặc default
    if not sys.stdin.isatty():
        try:
            input_data = json.load(sys.stdin)
        except json.JSONDecodeError:
            input_data = {}
    else:
        input_data = {
            "action": "calories_name_only",
            "exercise_name": "Push Up to Side Plank",
            "sets": 4,
            "reps": 12,
            "weight_kg": 68
        }

    action = input_data.get("action")
    result = {}

    try:
        if action == "calories_name_only":
            result = estimate_calories_by_name_only(
                engine,
                input_data.get("exercise_name"),
                int(input_data.get("sets", 0)),
                int(input_data.get("reps", 0)),
                float(input_data.get("weight_kg", 70))
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
                muscle=input_data.get("muscle"),
                equipment=input_data.get("equipment"),
                level=input_data.get("difficulty")
            )

        elif action == "get_exercise_info":
            # Sửa ở đây: KHÔNG gọi engine.get_exercise_by_name
            # Mà gọi hàm từ info_retriever.py
            ex_info = get_exercise_by_name(engine, input_data.get("exercise_name"))
            result = {
                "status": "success" if ex_info else "error",
                "exercise": ex_info,
                "message": "Không tìm thấy" if not ex_info else None
            }

        else:
            result = {"status": "error", "message": "Sai action"}

    except Exception as e:
        result = {"status": "error", "message": str(e)}

    result = fix_json_value(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))