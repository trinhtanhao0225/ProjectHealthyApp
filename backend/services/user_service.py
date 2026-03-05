# backend/services/user_service.py
from fastapi import HTTPException, status
from typing import List

from backend.models.user import User
from backend.schemas.user import UserCreate, UserResponse

from backend.utils.logger import logger

async def create_user(data: UserCreate) -> UserResponse:
    # Kiểm tra email đã tồn tại
    exists = await User.find_one(User.email == data.email)
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email đã tồn tại"
        )
    
    # Chuẩn hóa dữ liệu (giống code cũ)
    user_data = data.dict()
    user_data["allergies"] = user_data.get("allergies", [])
    user_data["diseases"] = user_data.get("diseases", [])
    user_data["bmr"] = user_data.get("bmr", 0)
    user_data["tdee"] = user_data.get("tdee", 0)
    
    user = User(**user_data)
    await user.insert()
    
    logger.info(f"User created: {data.email}")
    return UserResponse.from_orm(user)

async def get_all_users() -> List[UserResponse]:
    users = await User.find_all().to_list()
    return [UserResponse.from_orm(u) for u in users]

async def get_user_by_email(email: str) -> UserResponse:
    user = await User.find_one(User.email == email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy user"
        )
    
    return UserResponse.from_orm(user)