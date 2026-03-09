# backend/api/v1/endpoints/food.py
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from backend.schemas.food import FoodCreate, FoodResponse
from backend.services.food_service import save_food, get_all_foods, get_food_by_date

router = APIRouter(tags=["Food"])

@router.post("/", response_model=FoodResponse, status_code=201)
async def create_food(data: FoodCreate):
    return await save_food(data)

@router.get("/{email}", response_model=List[FoodResponse])
async def get_all_foods_by_email(email: str):
    return await get_all_foods(email)

@router.get("/date/{day}")
async def get_food_by_date(day: str, email: Optional[str] = Query(None)):
    return await get_food_by_date(day, email)