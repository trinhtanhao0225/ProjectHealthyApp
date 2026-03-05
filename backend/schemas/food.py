# backend/schemas/food.py
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

class NutritionSchema(BaseModel):
    calories_kcal: float = Field(0, ge=0)
    protein_g: float = Field(0, ge=0)
    carbohydrate_g: float = Field(0, ge=0)
    fat_g: float = Field(0, ge=0)

class FoodCreate(BaseModel):
    email: str = Field(..., description="Email người dùng")
    dish_name: str = Field(..., description="Tên món ăn")
    ingredients: List[str] = Field(default_factory=list, description="Danh sách nguyên liệu")
    portion_size: Optional[str] = Field("", description="Kích thước khẩu phần")
    nutrition: NutritionSchema = Field(default_factory=NutritionSchema, description="Thông tin dinh dưỡng")
    image_url: str = Field(..., description="URL ảnh từ Cloudinary")
    day: str = Field(..., description="Ngày (ví dụ: 2026-03-05 hoặc 'Thứ 3')")
    session: str = Field(..., description="Bữa ăn: Sáng/Trưa/Tối/Bữa nhẹ")
    is_recognized: bool = Field(False, description="Có phải từ nhận diện ảnh không")

class FoodResponse(BaseModel):
    id: Optional[str] = Field(None, description="ID document trong MongoDB")
    email: str
    dish_name: str
    ingredients: List[str]
    portion_size: str
    nutrition: NutritionSchema
    image_url: str
    day: str
    session: str
    is_recognized: bool
    createdAt: Optional[datetime] = None

    class Config:
        from_attributes = True