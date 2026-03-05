# backend/services/food_service.py
from fastapi import HTTPException
from typing import List, Optional

from backend.models.food import Food
from backend.schemas.food import FoodCreate, FoodResponse, NutritionSchema

from backend.utils.logger import logger

async def save_food(data: FoodCreate) -> FoodResponse:
    # Validate bắt buộc
    if not data.email:
        raise HTTPException(400, "Email is required")
    if not data.dish_name:
        raise HTTPException(400, "Tên món ăn không được để trống")
    if not data.image_url:
        raise HTTPException(400, "Image URL is required")
    if not data.day:
        raise HTTPException(400, "Ngày không được để trống")
    if not data.session:
        raise HTTPException(400, "Bữa ăn (session) không được để trống")

    # Chuẩn hóa dữ liệu (giống code Node cũ)
    food_data = {
        "email": data.email,
        "dish_name": str(data.dish_name),
        "ingredients": data.ingredients if isinstance(data.ingredients, list) else [],
        "portion_size": str(data.portion_size or ""),
        "nutrition": {
            "calories_kcal": float(data.nutrition.calories_kcal or 0),
            "protein_g": float(data.nutrition.protein_g or 0),
            "carbohydrate_g": float(data.nutrition.carbohydrate_g or 0),
            "fat_g": float(data.nutrition.fat_g or 0),
        },
        "image_url": str(data.image_url),
        "day": str(data.day),
        "session": str(data.session),
        "is_recognized": bool(data.is_recognized or False)
    }

    record = Food(**food_data)
    await record.insert()

    logger.info(f"Saved food for {data.email}: {data.dish_name}")
    return FoodResponse.from_orm(record)

async def get_all_foods(email: Optional[str] = None) -> List[FoodResponse]:
    query = {"email": email} if email else {}
    records = await Food.find(query).sort("-createdAt").to_list()

    return [FoodResponse.from_orm(r) for r in records]

async def get_food_by_date(day: str, email: Optional[str] = None) -> List[FoodResponse]:
    query = {"day": day}
    if email:
        query["email"] = email

    records = await Food.find(query).sort("-createdAt").to_list()

    return [FoodResponse.from_orm(r) for r in records]