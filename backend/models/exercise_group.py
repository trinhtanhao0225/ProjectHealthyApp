# backend/models/exercise_group.py
from beanie import Document

class ExerciseGroup(Document):
    email: str
    group_name: str

    class Settings:
        name = "ExerciseGroup"