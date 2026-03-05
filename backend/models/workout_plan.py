# backend/models/workout_plan.py
from beanie import Document

class WorkoutPlan(Document):
    email: str
    group_name: str
    day: str
    session: str
    done_flag: bool = False
    calories_burned: float = 0  # thêm để lưu calo khi mark done

    class Settings:
        name = "WorkoutPlan"