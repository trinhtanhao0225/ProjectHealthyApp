# backend/schemas/exercise.py
from pydantic import BaseModel, Field
from typing import List, Optional

class ExerciseDetailCreate(BaseModel):
    email: str = Field(..., description="Email người dùng")
    group_name: str = Field(..., description="Tên nhóm bài tập")
    name: str = Field(..., description="Tên bài tập")
    reps: int = Field(10, ge=1, description="Số lần lặp mỗi set")
    sets: int = Field(3, ge=1, description="Số set")

class ExerciseDetailResponse(BaseModel):
    id: Optional[str] = Field(None, description="ID document trong MongoDB")
    email: str
    group_name: str
    name: str
    reps: int
    sets: int

    class Config:
        from_attributes = True  # Hỗ trợ chuyển từ MongoDB document

class ExerciseGroupCreate(BaseModel):
    email: str = Field(..., description="Email người dùng")
    group_name: str = Field(..., description="Tên nhóm bài tập")

class ExerciseGroupResponse(BaseModel):
    id: Optional[str] = Field(None, description="ID document")
    email: str
    group_name: str

    class Config:
        from_attributes = True

class WorkoutPlanCreate(BaseModel):
    email: str = Field(..., description="Email người dùng")
    group_name: str = Field(..., description="Tên nhóm bài tập")
    day: str = Field(..., description="Ngày (ví dụ: 2026-03-05 hoặc 'Thứ 4')")
    session: str = Field(..., description="Buổi tập (Sáng/Trưa/Tối)")

class WorkoutPlanResponse(BaseModel):
    id: Optional[str] = Field(None, description="ID document")
    email: str
    group_name: str
    day: str
    session: str
    done_flag: bool = False
    calories_burned: float = Field(0, description="Tổng calo đốt khi hoàn thành")

    class Config:
        from_attributes = True

class ExerciseFilterParams(BaseModel):
    muscle: Optional[str] = Field(None, description="Nhóm cơ (chest, back, legs,...)")
    equipment: Optional[str] = Field(None, description="Thiết bị (barbell, dumbbell, bodyweight,...)")
    difficulty: Optional[float] = Field(None, description="Mức độ khó (thường là số từ cluster_label)")

class ExerciseInfoResponse(BaseModel):
    name: str = Field(..., description="Tên bài tập")
    MET: float = Field(..., description="MET value (Metabolic Equivalent of Task)")
    video: Optional[str] = Field(None, description="Link video hướng dẫn")
    instructions: Optional[str] = Field(None, description="Hướng dẫn thực hiện")
    equipment: Optional[List[str]] = Field(None, description="Danh sách thiết bị cần")
    muscles: Optional[List[str]] = Field(None, description="Nhóm cơ chính/phụ")

class CalorieEstimateResponse(BaseModel):
    exercise_name: str
    sets: int
    reps: int
    MET: float
    total_reps: int
    time_seconds: int
    calories: float = Field(..., description="Calo ước tính")

class GroupWithDetailsResponse(BaseModel):
    group: ExerciseGroupResponse
    details: List[ExerciseDetailResponse]

class PlanWithDetailsResponse(BaseModel):
    plan: WorkoutPlanResponse
    details: List[ExerciseDetailResponse]

# backend/schemas/exercise/action.py
from pydantic import BaseModel
from typing import Optional, Dict, Any

class ExerciseActionRequest(BaseModel):
    action: str = Field(..., description="Hành động: calories_name_only, muscles, equipment, difficulty, filter, get_exercise_info")
    exercise_name: Optional[str] = Field(None, description="Tên bài tập (bắt buộc cho calories_name_only và get_exercise_info)")
    sets: Optional[int] = Field(None, ge=0, description="Số set")
    reps: Optional[int] = Field(None, ge=0, description="Số reps")
    weight_kg: Optional[float] = Field(70, ge=30, description="Cân nặng (kg)")
    muscle: Optional[str] = Field(None, description="Nhóm cơ để lọc")
    equipment: Optional[str] = Field(None, description="Thiết bị để lọc")
    difficulty: Optional[float] = Field(None, description="Mức độ khó để lọc")

class ExerciseActionResponse(BaseModel):
    status: str = Field("success", description="success hoặc error")
    data: Dict[str, Any] = Field(default_factory=dict, description="Kết quả trả về tùy action")
    message: Optional[str] = Field(None, description="Thông báo lỗi hoặc thành công")