# backend/models/exercise_detail.py
from beanie import Document

class ExerciseDetail(Document):
    email: str
    group_name: str
    name: str
    reps: int = 10
    sets: int = 3

    class Settings:
        name = "ExerciseDetail"