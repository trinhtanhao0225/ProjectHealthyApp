# backend/models/user.py
from beanie import Document
from pydantic import EmailStr, Field
from typing import List, Optional

class User(Document):
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
    bmr: float = 0
    tdee: float = 0

    class Settings:
        name = "Users"