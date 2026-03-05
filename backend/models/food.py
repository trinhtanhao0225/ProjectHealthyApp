# backend/models/food.py
from beanie import Document
from pydantic import BaseModel
from typing import List
from datetime import datetime

class Nutrition(BaseModel):
    calories_kcal: float = 0
    protein_g: float = 0
    carbohydrate_g: float = 0
    fat_g: float = 0

class Food(Document):
    email: str
    dish_name: str
    ingredients: List[str] = []
    portion_size: str = ""
    nutrition: Nutrition = Nutrition()
    image_url: str
    day: str
    session: str
    is_recognized: bool = False
    createdAt: datetime = datetime.utcnow()
    updatedAt: datetime = datetime.utcnow()

    class Settings:
        name = "Food"
        indexes = [
            # Compound index cho email + day (tìm theo user + ngày)
            [("email", 1), ("day", 1)],
            # Compound index cho email + createdAt (descending để sort mới nhất)
            [("email", 1), ("createdAt", -1)]
        ]