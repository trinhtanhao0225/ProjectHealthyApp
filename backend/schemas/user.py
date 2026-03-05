# backend/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class UserCreate(BaseModel):
    email: EmailStr
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    age: Optional[int] = None
    target: Optional[str] = None
    targetWeight: Optional[float] = None
    exercise: Optional[str] = "—"
    allergies: List[str] = Field(default_factory=list)
    diseases: List[str] = Field(default_factory=list)
    caloriePlan: Optional[str] = "—"
    name: Optional[str] = None
    bmr: Optional[float] = 0
    tdee: Optional[float] = 0

class UserResponse(BaseModel):
    email: EmailStr
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    age: Optional[int] = None
    target: Optional[str] = None
    targetWeight: Optional[float] = None
    exercise: Optional[str] = "—"
    allergies: List[str]
    diseases: List[str]
    caloriePlan: Optional[str] = "—"
    name: Optional[str] = None
    bmr: float
    tdee: float

    class Config:
        from_attributes = True  # Hỗ trợ chuyển từ MongoDB document