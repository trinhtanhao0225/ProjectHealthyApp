from pydantic import BaseModel
from typing import Optional, Dict, Any

class UserInfo(BaseModel):
    user_id: str
    age: Optional[int] = None
    gender: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    goal: Optional[str] = None
    allergies: list[str] = []
    diseases: list[str] = []

class QueryRequest(BaseModel):
    query: str
    user_info: Optional[UserInfo] = None