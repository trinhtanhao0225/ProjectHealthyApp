# backend/schemas/exercise.py
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime


# ----------------- GROUP -----------------
class ExerciseGroupCreate(BaseModel):
    email: str = Field(..., description="Email người dùng (bắt buộc)")
    group_name: str = Field(..., min_length=1, description="Tên nhóm bài tập (bắt buộc, không rỗng)")

    class Config:
        schema_extra = {
            "example": {
                "email": "user1@gmail.com",
                "group_name": "Nhóm Full Body"
            }
        }


class ExerciseGroupResponse(BaseModel):
    id: Optional[str] = Field(None, description="ID ObjectId dưới dạng string")
    email: str
    group_name: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "65f8b123456789abcdef1234",
                "email": "user1@gmail.com",
                "group_name": "Nhóm Full Body",
                "created_at": "2026-03-07T00:00:00"
            }
        }


# ----------------- DETAIL -----------------
class ExerciseDetailCreate(BaseModel):
    email: str = Field(..., description="Email người dùng")
    group_name: str = Field(..., description="Tên nhóm bài tập")
    name: str = Field(..., min_length=1, description="Tên bài tập")
    sets: int = Field(3, ge=1, description="Số set (ít nhất 1)")
    reps: int = Field(10, ge=1, description="Số reps mỗi set (ít nhất 1)")

    class Config:
        schema_extra = {
            "example": {
                "email": "user1@gmail.com",
                "group_name": "Nhóm Full Body",
                "name": "Push-up",
                "sets": 4,
                "reps": 15
            }
        }


class ExerciseDetailResponse(BaseModel):
    id: Optional[str] = Field(None, description="ID ObjectId dưới dạng string")
    email: str
    group_name: str
    name: str
    sets: int
    reps: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "65f8b123456789abcdef5678",
                "email": "user1@gmail.com",
                "group_name": "Nhóm Full Body",
                "name": "Push-up",
                "sets": 4,
                "reps": 15,
                "created_at": "2026-03-07T00:00:00"
            }
        }


# ----------------- WORKOUT PLAN -----------------
class WorkoutPlanCreate(BaseModel):
    email: str = Field(..., description="Email người dùng")
    group_name: str = Field(..., description="Tên nhóm bài tập")
    day: str = Field(..., description="Ngày tập (ví dụ: '2026-03-07' hoặc 'Thứ Hai')")
    session: str = Field(..., description="Buổi tập (Sáng, Trưa, Tối, A, B...)")

    class Config:
        schema_extra = {
            "example": {
                "email": "user1@gmail.com",
                "group_name": "Nhóm Full Body",
                "day": "2026-03-07",
                "session": "Sáng"
            }
        }


class WorkoutPlanResponse(BaseModel):
    id: Optional[str] = Field(None, description="ID ObjectId dưới dạng string")
    email: str
    group_name: str
    day: str
    session: str
    done_flag: bool = False
    calories_burned: float = Field(0.0, description="Tổng calo đốt khi hoàn thành buổi tập")
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ----------------- FILTER & INFO -----------------
class ExerciseFilterParams(BaseModel):
    muscle: Optional[str] = Field(None, description="Nhóm cơ (chest, back, legs, quads,...)")
    equipment: Optional[str] = Field(None, description="Thiết bị (barbell, dumbbell, bodyweight, none,...)")
    difficulty: Optional[int] = Field(None, description="Mức độ khó (1-5)")

    class Config:
        schema_extra = {
            "example": {
                "muscle": "quads",
                "equipment": "none",
                "difficulty": 3
            }
        }


class ExerciseInfoResponse(BaseModel):
    name: str = Field(..., description="Tên bài tập")
    MET: Optional[float] = Field(None, description="MET value")
    video: Optional[str] = Field(None, description="Link video hướng dẫn")
    instructions: Optional[str] = Field(None, description="Hướng dẫn thực hiện")
    equipment: Optional[List[str]] = Field(None, description="Danh sách thiết bị")
    combined_muscles: Optional[List[str]] = Field(None, description="Nhóm cơ liên quan")
    category: Optional[str] = Field(None, description="Loại bài tập (strength, cardio,...)")

    class Config:
        from_attributes = True


class CalorieEstimateResponse(BaseModel):
    exercise_name: str
    sets: int
    reps: int
    MET: float
    total_reps: int
    time_seconds: Optional[int] = None
    calories: float = Field(..., description="Calo ước tính")


# ----------------- RESPONSE TỔNG HỢP -----------------
class GroupWithDetailsResponse(BaseModel):
    group: ExerciseGroupResponse
    details: List[ExerciseDetailResponse]


class PlanWithDetailsResponse(BaseModel):
    plan: WorkoutPlanResponse
    details: List[ExerciseDetailResponse]


# ----------------- ACTION REQUEST (CHO CÁC HÀNH ĐỘNG TỔNG HỢP) -----------------
class ExerciseActionRequest(BaseModel):
    action: str = Field(..., description="Loại hành động: create_group, add_detail, mark_done, ...")

    email: Optional[str] = Field(None, description="Email người dùng")
    group_name: Optional[str] = Field(None, description="Tên nhóm")
    day: Optional[str] = Field(None, description="Ngày tập")
    session: Optional[str] = Field(None, description="Buổi tập")

    exercise_name: Optional[str] = Field(None, description="Tên bài tập")
    sets: Optional[int] = Field(None, ge=1)
    reps: Optional[int] = Field(None, ge=1)
    weight_kg: Optional[float] = Field(70.0, ge=0)

    details: Optional[List[Dict[str, Any]]] = Field(None, description="Danh sách detail khi tạo nhóm + nhiều bài cùng lúc")

    @validator("action")
    def validate_action(cls, v):
        allowed = ["create_group", "add_detail", "create_plan", "mark_done", "calculate_calories"]
        if v not in allowed:
            raise ValueError(f"Action phải là một trong: {', '.join(allowed)}")
        return v


class ExerciseActionResponse(BaseModel):
    status: str = Field(..., description="success / error")
    data: Optional[Any] = None
    message: Optional[str] = None


class ExercisesResponse(BaseModel):
    success: bool = True
    data: List[ExerciseDetailResponse] = Field(..., description="Danh sách bài tập chi tiết")